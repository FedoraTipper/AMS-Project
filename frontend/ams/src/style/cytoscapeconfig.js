module.exports.config = [{
  "selector": "node",
  "style": {
    "shape": "hexagon",
    "background-color": "#0d47a1",
    "label": "data(name)",
    "background-image": "data(imglink)",
    "background-fit": "cover",
    "height": 24,
    "width": 24
  }
},
{
  "selector": "edge",
  "style": {
    "line-color": "#42a5f5",
    "label": "data(name)",
    'curve-style': 'straight',
    "target-arrow-color": "#0d47a1",
    "target-arrow-shape": "triangle"
  }
},
{
  "selector": ".eh-handle",
  "style": {
    "background-color": "red",
    "width": 12,
    "height": 12,
    "shape": "ellipse",
    "overlay-opacity": 0,
    "border-width": 12, // makes the handle easier to hit
    "border-opacity": 0
  }
},
{
  "selector": ".eh-hover",
  "style": {
    "background-color": "red"
  }
},
{
  "selector": ".eh-source",
  "style": {
    "border-width": 2,
    "border-color": "red"
  }
},
{
  "selector": ".eh-target",
  "style": {
    "border-width": 2,
    "border-color": "red"
  }
},
{
  "selector": ".eh-preview, .eh-ghost-edge",
  "style": {
    "background-color": "red",
    "line-color": "red",
    "target-arrow-color": "red",
    "source-arrow-color": "red"
  }
},
{
  "selector": ".eh-ghost-edge.eh-preview-active",
  "style": {
    "opacity": 0
  }
},
{
  "selector": "edge[name]",
  "style": {
    "label": "data(name)"
  }
},
{
  "selector": ":selected",
  "style": {
    "border-width": 3,
    "border-color": "#DAA520"
  }
}]