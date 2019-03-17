import axios from 'axios';

export function load_assets(type_array, type_count, view_array, current_view, label_array,
    relationship_array, auth_header, cy) {
    return new Promise(function (resolve, reject) {
        const requests = [
            axios({
                url: "http://127.0.0.1:5000/api/view/",
                headers: auth_header,
                method: "get"
            }),
            axios({
                url: "http://127.0.0.1:5000/api/type/",
                headers: auth_header,
                method: "get"
            }),
            axios({
                url: "http://127.0.0.1:5000/api/label/",
                headers: auth_header,
                method: "get"
            }),
            axios({
                url: "http://127.0.0.1:5000/api/node/",
                headers: auth_header,
                method: "get"
            }), axios({
                url: "http://127.0.0.1:5000/api/relationship/",
                headers: auth_header,
                method: "get"
            }),
            axios({
                url: "http://127.0.0.1:5000/api/link/",
                headers: auth_header,
                method: "get"
            })
        ];
        Promise.all(requests).then(values => {
            let views = values[0].data["data"];
            for (let i = 0; i < views.length; i++) {
                view_array.push(views[i])
            }
            current_view.name = view_array[0].name
            current_view.id = view_array[0].view_id
            let types = values[1].data["data"];
            let types_dict = {}
            for (let i = 0; i < types.length; i++) {
                type_array.push(types[i])
                types_dict[types[i].type_id] = types[i].type
            }
            let label_dict = {}
            let labels = values[2].data["data"];
            for (let i = 0; i < labels.length; i++) {
                label_array.push(labels[i])
                label_dict[labels[i].label_id] = labels[i].label_text
            }
            let nodes = values[3].data["data"];
            for (let i = 0; i < nodes.length; i++) {
                if (nodes[i].view_id == current_view.id) {
                    let node_name = ""
                    if (nodes[i].label_id == null) {
                        let count = 0
                        if (type_count[types_dict[nodes[i].type_id]] == null) {
                            type_count[types_dict[nodes[i].type_id]] = 1
                            count = 1;
                        } else {
                            count = ++type_count[types_dict[nodes[i].type_id]];
                        }
                        node_name = types_dict[nodes[i].type_id] + " " + count
                    } else {
                        node_name = label_dict[nodes[i].label_id]
                    }
                    cy.add({
                        group: "nodes",
                        data: {
                            id: nodes[i].node_id,
                            name: node_name,
                            payload: {
                                type_id: nodes[i].type_id,
                                type: types_dict[nodes[i].type_id],
                                view_id: current_view.id,
                                label_id: nodes[i].label_id,
                                label_text: label_dict[nodes[i].label_id]
                            },
                            imglink: null
                        }
                    });
                }
            }
            let relationships = values[4].data["data"]
            let relationship_dict = {}
            for (let i = 0; i < relationships.length; i++) {
                relationship_array.push(relationships[i]);
                relationship_dict[relationships[i].relationship_id] = relationships[i].message
            }
            let links = values[5].data["data"];
            for (let i = 0; i < links.length; i++) {
                if (links[i].view_id == current_view.id) {
                    cy.add({
                        group: "edges",
                        data: {
                            id: "l" + links[i].link_id,
                            name: relationship_dict[links[i].relationship_id],
                            source: links[i].node_id_1,
                            target: links[i].node_id_2,
                            payload: {
                                relationship_id: relationship_dict[links[i].relationship_id],
                                view_id: links[i].view_id
                            }
                        }
                    });
                }
            }
        });
        setTimeout(resolve, 2500)
    });
}

export function add_node(node_details, node_type, current_view, auth_header, cy) {
    return new Promise(function (resolve, reject) {
        let returned_id = ""
        axios({
            url: "http://127.0.0.1:5000/api/node/",
            headers: auth_header,
            method: "post",
            data: node_details
        }).then(response => {
            if (response.data["message"].includes("Success")) {
                returned_id = response.data["payload"];
                cy.add({
                    group: "nodes",
                    data: {
                        id: returned_id,
                        name: node_type,
                        payload: {
                            type_id: node_details["type_id"],
                            type: node_type,
                            view_id: current_view.id
                        },
                        imglink: null
                    }
                });
            } else {
                alert("Failed to create new node. " + response.data["message"]);
            }
        });
        setTimeout(resolve, 3500);
        cy.$id(returned_id).select();
    });


}

export function delete_node(node_details, node, auth_header, cy) {
    axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: auth_header,
        method: "delete",
        data: node_details
    }).then(response => {
        if (response.data["message"].includes("Success")) {
            cy.remove(node);
            return true;
        } else {
            alert("Failed to delete node. " + response.data["message"]);
            return false;
        }
    });
}

export function delete_link(link_details, link, auth_header, cy) {
    axios({
        url: "http://127.0.0.1:5000/api/link/",
        headers: auth_header,
        method: "delete",
        data: link_details
    }).then(response => {
        if (response.data["message"].includes("Success")) {

            cy.remove(link);
            return true

        } else {
            alert("Failed to delete node. " + response.data["message"]);
            return false;
        }
    });
}