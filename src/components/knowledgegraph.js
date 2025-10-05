import { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';
import './knowledgegraph.css';

function KnowledgeGraph() {
  const cyRef = useRef(null);
  const containerRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    // TEST DATA - Remove this and uncomment fetch below when backend is ready
    const testData = [
      {
        id: 1,
        title: "Microgravity Effects on Mouse Bone Structure",
        authors: "Smith et al.",
        year: "2013",
        keywords: "microgravity, bone loss, osteocytes, spaceflight, mice"
      },
      {
        id: 2,
        title: "Cardiovascular Adaptation in Space Missions",
        authors: "Johnson et al.",
        year: "2014",
        keywords: "cardiovascular, microgravity, adaptation, heart, spaceflight"
      },
      {
        id: 3,
        title: "Immune System Response to Microgravity",
        authors: "Williams et al.",
        year: "2013",
        keywords: "immune system, microgravity, t-cells, spaceflight, health"
      },
      {
        id: 4,
        title: "Muscle Atrophy During Extended Spaceflight",
        authors: "Brown et al.",
        year: "2014",
        keywords: "muscle atrophy, microgravity, spaceflight, exercise, countermeasures"
      },
      {
        id: 5,
        title: "Regenerative Medicine Applications in Microgravity",
        authors: "Davis et al.",
        year: "2024",
        keywords: "regenerative medicine, stem cells, microgravity, cardiomyocytes, therapy"
      },
      {
        id: 6,
        title: "Cancer Cell Behavior in Microgravity Environment",
        authors: "Martinez et al.",
        year: "2024",
        keywords: "cancer, microgravity, spheroids, oncology, research"
      }
    ];

    // Small delay to ensure DOM is ready
    setTimeout(() => {
      if (mounted && containerRef.current) {
        initializeCytoscape(testData);
        setLoading(false);
      }
    }, 100);

    // REAL BACKEND FETCH - Uncomment this when your backend is ready
    fetch('http://localhost:5000/data')
      .then(response => response.json())
      .then(data => {
        if (mounted && containerRef.current) {
          initializeCytoscape(data);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching data:', err);
        if (mounted) {
          setError('Failed to load publications data');
          setLoading(false);
        }
      });

    // Cleanup
    return () => {
      mounted = false;
      if (cyRef.current) {
        try {
          cyRef.current.destroy();
          cyRef.current = null;
        } catch (e) {
          console.log('Cleanup error:', e);
        }
      }
    };
  }, []);

  const initializeCytoscape = (publications) => {
    // Destroy existing instance if it exists
    if (cyRef.current) {
      try {
        cyRef.current.destroy();
        cyRef.current = null;
      } catch (e) {
        console.log('Error destroying previous instance:', e);
      }
    }

    // Check if container still exists
    if (!containerRef.current) {
      console.log('Container not available');
      return;
    }

    const elements = buildGraphElements(publications);

    try {
      cyRef.current = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node[type="publication"]',
          style: {
            'background-color': '#4CAF50',
            'label': 'data(label)',
            'width': 40,
            'height': 40,
            'font-size': '10px',
            'text-wrap': 'wrap',
            'text-max-width': '100px',
            'text-valign': 'bottom',
            'text-halign': 'center',
            'color': '#ffffff',
            'text-outline-color': '#171738',
            'text-outline-width': 2
          }
        },
        {
          selector: 'node[type="year"]',
          style: {
            'background-color': '#2196F3',
            'label': 'data(label)',
            'width': 60,
            'height': 60,
            'font-size': '14px',
            'font-weight': 'bold',
            'color': '#ffffff',
            'text-outline-color': '#171738',
            'text-outline-width': 2,
            'shape': 'diamond'
          }
        },
        {
          selector: 'node[type="keyword"]',
          style: {
            'background-color': '#FF9800',
            'label': 'data(label)',
            'width': 30,
            'height': 30,
            'font-size': '9px',
            'color': '#ffffff',
            'text-outline-color': '#171738',
            'text-outline-width': 2,
            'shape': 'ellipse'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#666',
            'target-arrow-color': '#666',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'opacity': 0.6
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 3,
            'border-color': '#FFF'
          }
        }
      ],
      layout: {
        name: 'cose',
        idealEdgeLength: 100,
        nodeOverlap: 20,
        refresh: 20,
        fit: true,
        padding: 30,
        randomize: false,
        componentSpacing: 100,
        nodeRepulsion: 400000,
        edgeElasticity: 100,
        nestingFactor: 5,
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95,
        minTemp: 1.0
      },
      minZoom: 0.3,
      maxZoom: 3
    });

    // Add click event to show publication details
    cyRef.current.on('tap', 'node[type="publication"]', (evt) => {
      const node = evt.target;
      const pub = node.data('publication');
      alert(`Title: ${pub.title}\nYear: ${pub.year}\nAuthors: ${pub.authors}`);
    });
    } catch (e) {
      console.error('Error initializing Cytoscape:', e);
      setError('Failed to initialize graph');
    }
  };

  const buildGraphElements = (publications) => {
    const elements = [];
    const yearNodes = new Set();
    const keywordNodes = new Map();
    const maxKeywordsPerPub = 5;

    // First pass: collect all years and keywords
    publications.forEach(pub => {
      if (pub.year && pub.year !== 'Unknown') {
        yearNodes.add(pub.year);
      }
      
      if (pub.keywords) {
        const keywords = pub.keywords.split(',').map(k => k.trim().toLowerCase());
        keywords.forEach(kw => {
          if (kw && kw.length > 3) {
            keywordNodes.set(kw, (keywordNodes.get(kw) || 0) + 1);
          }
        });
      }
    });

    // Get top keywords by frequency
    const topKeywords = Array.from(keywordNodes.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20)
      .map(([kw]) => kw);

    // Add year nodes
    yearNodes.forEach(year => {
      elements.push({
        data: {
          id: `year-${year}`,
          label: year,
          type: 'year'
        }
      });
    });

    // Add keyword nodes
    topKeywords.forEach(keyword => {
      elements.push({
        data: {
          id: `keyword-${keyword}`,
          label: keyword,
          type: 'keyword'
        }
      });
    });

    // Add publication nodes and edges
    publications.forEach((pub, index) => {
      const pubId = `pub-${index}`;
      
      // Add publication node
      elements.push({
        data: {
          id: pubId,
          label: pub.title.substring(0, 30) + '...',
          type: 'publication',
          publication: pub
        }
      });

      // Connect to year
      if (pub.year && pub.year !== 'Unknown' && yearNodes.has(pub.year)) {
        elements.push({
          data: {
            id: `edge-${pubId}-year-${pub.year}`,
            source: pubId,
            target: `year-${pub.year}`
          }
        });
      }

      // Connect to keywords
      if (pub.keywords) {
        const keywords = pub.keywords.split(',')
          .map(k => k.trim().toLowerCase())
          .filter(k => topKeywords.includes(k))
          .slice(0, maxKeywordsPerPub);

        keywords.forEach(keyword => {
          elements.push({
            data: {
              id: `edge-${pubId}-keyword-${keyword}`,
              source: pubId,
              target: `keyword-${keyword}`
            }
          });
        });
      }
    });

    return elements;
  };

  const handleReset = () => {
    if (cyRef.current) {
      cyRef.current.fit();
      cyRef.current.zoom(1);
    }
  };

  const handleReLayout = () => {
    if (cyRef.current) {
      cyRef.current.layout({
        name: 'cose',
        animate: true,
        animationDuration: 1000
      }).run();
    }
  };

  return (
    <div className="knowledge-graph-main">
      <div className="knowledge-graph-content" ref={containerRef}>
        {loading && (
          <div className="loading-overlay">
            <p>Loading knowledge graph...</p>
          </div>
        )}
        {error && (
          <div className="error-overlay">
            <p>{error}</p>
          </div>
        )}
        
        {!loading && !error && (
          <>
            <div className="graph-legend">
              <h4>Legend</h4>
              <div className="legend-item">
                <div className="legend-color publication"></div>
                <span>Publications</span>
              </div>
              <div className="legend-item">
                <div className="legend-color year"></div>
                <span>Years</span>
              </div>
              <div className="legend-item">
                <div className="legend-color keyword"></div>
                <span>Keywords</span>
              </div>
            </div>
            
            <div className="graph-controls">
              <button onClick={handleReset}>Reset View</button>
              <button onClick={handleReLayout}>Re-layout</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default KnowledgeGraph;