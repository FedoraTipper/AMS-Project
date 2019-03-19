export function expand_node(node, cy) {
    let neighbours = this.get_neighbours(
        node.data("id"),
        cy
    );
    for (let i = 0; i < neighbours.length; i++) {
        neighbours[i]["_private"]["data"]["display"] = "element";
        neighbours[i].show();
    }
}

export function collapse_node(node, cy) {
    let indegrees = this.get_indegrees_nodes(
        node.data("id"),
        cy
    );
    let explored = {};
    explored[node.data("id")] = 1;
    for (let i = 0; i < indegrees.length; i++) {
        if (explored[indegrees[i].data("id")] == undefined) {
            this.hide_recursively(
                indegrees[i],
                explored,
                cy
            );
        }
    }
}

export function hide_recursively(node, explored, cy) {
    let neighbours = this.get_neighbours(node.data("id"), cy);
    if (neighbours.length == 0) {
        node["_private"]["data"]["display"] = "none";
        explored[node.data("id")] = 1;
        node.show();
        node.hide();
    } else {
        node["_private"]["data"]["display"] = "none";
        explored[node.data("id")] = 1;
        for (let i = 0; i < neighbours.length; i++) {
            if (explored[neighbours[i].data("id")] == undefined) {
                this.hide_recursively(neighbours[i], explored, cy);
            }
        }
    }
}

export function get_indegrees_nodes(node_id, cy) {
    let edges = cy.edges("[target = '" + node_id + "']");
    let nodes = [];
    for (let i = 0; i < edges.length; i++) {
        let source_node = window.cy.$id(edges.data("source"));
        nodes.push(source_node);
    }
    return nodes;
}

export function get_neighbours(node_id, cy) {
    let nodes = [];
    let elements = cy.$id(String(node_id)).neighborhood();
    for (let i = 0; i < elements.length; i++) {
        if (elements[i].isNode()) {
            nodes.push(elements[i]);
        }
    }
    return nodes;
}

export function build_search_list(cy) {
    let search_list = []
    let nodes = cy.nodes();
    for (let i = 0; i < nodes.length; i++) {
        let node_details = nodes[i]["_private"]["data"];
        let node_search_details = {
            node_id: node_details["id"],
            node_name: node_details["name"],
            node_type: node_details["payload"]["type"],
            label_text: node_details["payload"]["label_text"]
        };
        search_list.push(node_search_details);
    }
    return search_list;
}