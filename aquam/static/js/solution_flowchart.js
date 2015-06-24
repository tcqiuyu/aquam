/**
 * Created by Qiu Yu on 6/24/2015.
 */
var graph = new joint.dia.Graph;

var paper = new joint.dia.Paper({
    el: $('#flowchart'),
    width: 1130,
    height: 600,
    model: graph,
    gridSize: 1,
    interactive: false
});

joint.shapes.custom = {};

joint.shapes.custom.ElementLink = joint.shapes.basic.Rect.extend({
    markup: '<a><g class="rotatable"><g class="scalable"><rect/></g><text/></g></a>',
    defaults: joint.util.deepSupplement({
        type: 'custom.ElementLink'
    }, joint.shapes.basic.Rect.prototype.defaults)
});


var background_frame_1 = new joint.shapes.custom.ElementLink({
    position: {x: 1, y: 10},
    size: {width: 760, height: 580},
    attrs: {
        rect: {fill: 'transparent', stroke: '#2D69A6', "stroke-dasharray": "5,5", cursor: 'default'}
    }
});

var background_frame_2 = new joint.shapes.custom.ElementLink({
    position: {x: 770, y: 180},
    size: {width: 359, height: 220},
    attrs: {
        rect: {fill: 'transparent', stroke: '#9F3034', "stroke-dasharray": "5,5", cursor: 'default'}
    }
});

var background_frame_3 = new joint.shapes.custom.ElementLink({
    position: {x: 412, y: 410},
    size: {width: 200, height: 130},
    attrs: {
        rect: {fill: 'transparent', stroke: '#13B038', "stroke-dasharray": "5,5", cursor: 'default'}
    }
});
var x_start = 10;

var node_1 = new joint.shapes.custom.ElementLink({
    position: {x: x_start, y: 100},
    size: {width: 160, height: 80},
    attrs: {
        rect: {fill: '#2D69A6'},
        a: {'xlink:href': 'water-use-analyzer/demo/', 'xlink:show': 'new', cursor: 'pointer'},
        text: {text: 'Fresh Water\n    Source', fill: 'white', 'font-size': 21}
    }
});

var node_2 = node_1.clone();
node_2.translate(240, 160);
node_2.attr({
    text: {text: '  Drilling/\nFracturing'}
});

var node_3 = node_1.clone();
node_3.translate(0, 320);
node_3.attr({
    text: {text: '  Alternative\nSurface  Use'}
});

var node_4 = node_2.clone();
node_4.translate(340);
node_4.attr({
    text: {text: '   Produced\nWater Storage'}
});

var node_5 = node_3.clone();
node_5.translate(420);
node_5.attr({
    text: {text: 'Treatment'}
});

var node_6 = node_4.clone();
node_6.translate(350);
node_6.attr({
    text: {text: 'Disposal'}
});

var link_1_2 = new joint.dia.Link({
    source: {x: x_start + 80, y: 180},
    target: {x: x_start + 240, y: 300},
    vertices: [{x: x_start + 80, y: 300}],
    attrs: {
        '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}
    },
    labels: [
        {
            position: .7,
            attrs: {
                text: {
                    text: 'V<sub>frac</sub>\nWQ<sub>frac</sub>',
                    fill: 'black',
                    "font-size": 15
                }
            }
        }
    ]
});

var link_2_4 = new joint.dia.Link({
    source: {x: x_start + 400, y: 300},
    target: {x: x_start + 580, y: 300},
    attrs: {
        '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}
    },
    labels: [
        {
            position: .5,
            attrs: {
                text: {
                    text: 'V<sub>produced</sub>\nWQ<sub>produced</sub>\nT<sub>produced</sub>',
                    fill: 'black',
                    "font-size": 15
                }
            }
        }
    ]
});

var link_4_5 = new joint.dia.Link({
    source: {x: x_start + 660, y: 340},
    target: {x: x_start + 580, y: 460},
    vertices: [{x: x_start + 660, y: 460}],
    attrs: {
        '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}
    },
    labels: [
        {
            position: .37,
            attrs: {
                text: {
                    text: 'V<sub>treatment</sub>\nWQ<sub>treatment</sub>\nT<sub>treatment</sub>',
                    fill: 'black',
                    "font-size": 15
                }
            }
        }
    ]
});

var link_4_6 = new joint.dia.Link({
    source: {x: x_start + 740, y: 300},
    target: {x: x_start + 930, y: 300},
    attrs: {
        '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}
    },
    labels: [
        {
            position: .6,
            attrs: {
                text: {
                    text: 'V<sub>disposal</sub>\nWQ<sub>produced</sub>\nT<sub>disposal</sub>',
                    fill: 'black',
                    "font-size": 15
                }
            }
        }
    ]
});

var link_5_3 = new joint.dia.Link({
    source: {x: x_start + 420, y: 460},
    target: {x: x_start + 160, y: 460},
    attrs: {
        '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}
    },
    labels: [
        {
            position: .74,
            attrs: {
                text: {
                    text: 'V<sub>surface</sub>\nWQ<sub>surface</sub>\nT<sub>surface</sub>',
                    fill: 'black',
                    "font-size": 15
                }
            }
        }
    ]
});

var link_5_2 = new joint.dia.Link({
    source: {x: x_start + 420, y: 460},
    target: {x: x_start + 240, y: 300},
    vertices: [{x: x_start + 380, y: 460}, {x: x_start + 380, y: 400}, {x: x_start + 80, y: 400}, {
        x: x_start + 80,
        y: 300
    }],
    attrs: {
        '.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}
    },
    labels: [
        {
            position: .25,
            attrs: {
                text: {
                    text: 'V<sub>recycle</sub>\nWQ<sub>recycle</sub>\nT<sub>recycle</sub>',
                    fill: 'black',
                    "font-size": 15
                }
            }
        }
    ]
});

var subtitle_1 = new joint.shapes.custom.ElementLink({
    position: {x: x_start + 220, y: 30},
    size: {width: 340, height: 35},
    attrs: {
        rect: {fill: "transparent", stroke: '#2D69A6', "stroke-width": 2.5, cursor: 'default'},
        text: {text: 'Water management Technology', fill: 'black', 'font-size': 20, cursor: 'default'}
    }
});

var subtitle_2 = new joint.shapes.custom.ElementLink({
    position: {x: x_start + 770, y: 200},
    size: {width: 340, height: 35},
    attrs: {
        rect: {fill: "transparent", stroke: '#B13337', "stroke-width": 2.5, cursor: 'default'},
        text: {text: 'Minimize by Alternative Surface Use', fill: 'black', 'font-size': 20, cursor: 'default'}
    }
});

var note_1 = new joint.shapes.custom.ElementLink({
    position: {x: x_start + 130, y: 80},
    attrs: {
        rect: {fill: "transparent", stroke: "transparent", cursor: 'default'},
        text: {text: 'C<sub>fresh</sub>', fill: 'black', 'font-size': 16, 'font-weight': "bold", cursor: 'default'}
    }
});

var note_2 = note_1.clone();
note_2.translate(110, 35);
note_2.attr({
    text: {text: 'V<sub>fresh</sub>'}
});

var note_3 = note_2.clone();
note_3.translate(5, 25);
note_3.attr({
    text: {text: 'WQ<sub>fresh</sub>'}
});

var note_4 = note_3.clone();
note_4.translate(-5, 25);
note_4.attr({
    text: {text: 'T<sub>fresh</sub>'}
});

var note_5 = note_4.clone();
note_5.translate(310, 350);
note_5.attr({
    text: {text: 'C<sub>treatment</sub>'}
});

var note_6 = note_4.clone();
note_6.translate(820, 190);
note_6.attr({
    text: {text: 'C<sub>disposal</sub>'}
});

graph.addCells([background_frame_1, background_frame_2, background_frame_3, subtitle_1, subtitle_2, node_1, node_2,
    node_3, node_4, node_5, node_6, link_5_2, link_1_2, link_2_4, link_4_5, link_4_6, link_5_3, note_1, note_2, note_3,
    note_4, note_5, note_6]);

$("text").each(function () {
    var $this = $(this);
    var t = $this.html();
    //correctly present subscript text
    $this.html(t.replace("&lt;sub&gt;", "<tspan baseline-shift=\"sub\" dy=\"-0.1em\">")
        .replace("&lt;/sub&gt;", "</tspan>"));
});

$(".label tspan").each(function () {
    var $this = $(this);
    var t = $this.html();
    //correctly present subscript text
    $this.html(t.replace("&lt;sub&gt;", "<tspan baseline-shift=\"sub\" dy=\"-0.1em\">")
        .replace("&lt;/sub&gt;", "</tspan>"));
    //tweek the position of multi-line text, so that they won't overlap each other
    $this.attr("dy", function (i, origValue) {
        if (origValue != "0em") {
            return "2em";
        } else {
            return "-1em";
        }
    })
});

$(".label > rect").each(function () {
    var $this = $(this);
    var offset = 90;
    //tweek the background of link text
    $this.attr("width", function (i, origValue) {//
        return origValue - offset;
    });
    $this.attr("height", 90);
    $this.attr("x", function (i, origValue) {
        return parseInt(origValue) + 1 / 2 * offset;
    });
    $this.attr("y", function (i, origValue) {
        return parseInt(origValue) - 1 / 4 * offset;
    });
});