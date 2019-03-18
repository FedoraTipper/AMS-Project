import axios from 'axios';

export function load_assets(type_array, view_array, current_view, label_array, relationship_array, auth_header, cy) {
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
            cy.elements().remove();
            let type_count = {}
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
                                label_text: label_dict[nodes[i].label_id],
                                icon: nodes[i].icon
                            },
                            imglink: "https://cors-anywhere.herokuapp.com/" + nodes[i].icon
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
                                link_id: links[i].link_id,
                                relationship_id: links[i].relationship_id,
                                relationship_message: relationship_dict[links[i].relationship_id],
                                view_id: links[i].view_id
                            }
                        }
                    });
                }
            }
            resolve({
                "dicts": [types_dict, label_dict, relationship_dict],
                "arrays": [type_array, label_array, relationship_array]
            })
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
        setTimeout(resolve, 4000);
        cy.$id(returned_id).select();
    });
}

export function change_node(node_details, label_text, type_name, auth_header, cy) {
    return new Promise(function (resolve) {
        axios({
            url: "http://127.0.0.1:5000/api/node/",
            headers: auth_header,
            method: "put",
            data: node_details
        }).then(response => {
            if (response.data["message"].includes("Success")) {
                let node = cy.getElementById(node_details["node_id"])
                let name = null
                if (node_details["type_id"]) {
                    name = type_name;
                    node["_private"]["data"]["payload"]["type_id"] = node_details["type_id"]
                    node["_private"]["data"]["payload"]["type"] = type_name;
                }
                if (node_details["label_id"]) {
                    name = label_text
                    node["_private"]["data"]["payload"]["label_id"] = node_details["label_id"]
                    node["_private"]["data"]["payload"]["label_text"] = label_text
                }
                if (node_details["icon"]) {
                    node["_private"]["data"]["imglink"] = "https://cors-anywhere.herokuapp.com/" + node_details["icon"]
                }
                if (name) {
                    node["_private"]["data"]["name"] = name;
                }
                resolve(true)
            } else {
                alert("Change to link failed")
                resolve(false)
            }
        })
    })

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

export function add_link(link_details, premade_link_obj, auth_header, cy) {
    return new Promise(function (resolve) {
        try {
            axios({
                url: "http://127.0.0.1:5000/api/link/",
                headers: auth_header,
                method: "post",
                data: link_details
            }).then(response => {
                if (response.data["message"].includes("Success")) {
                    let returned_id = response.data["payload"]
                    premade_link_obj[0]["_private"]["data"]["id"] = "l" + returned_id
                    premade_link_obj[0]["_private"]["data"]["payload"] = {
                        link_id: returned_id
                    }
                    resolve(true)
                } else {
                    alert("Failed to delete node. " + response.data["message"]);
                    cy.remove(premade_link_obj);
                    resolve(false);
                }
            });
        } catch{
            //Since adding a link is a leading action. If anything fails, it needs to be deleted.
            alert("Something went wrong, reverting link")
            cy.remove(premade_link_obj);
            resolve(false)
        }

    });
}

export function change_link(link_details, relationship_message, auth_header, cy) {
    axios({
        url: "http://127.0.0.1:5000/api/link/",
        headers: auth_header,
        method: "put",
        data: link_details
    }).then(response => {
        if (response.data["message"].includes("Success")) {
            let link = cy.getElementById("l" + link_details["link_id"])
            link["_private"]["data"]["name"] = relationship_message;
        } else {
            alert("Change to link failed")
        }
    })
}

export function delete_link(link_details, link, auth_header, cy) {
    return new Promise(function (resolve, reject) {
        axios({
            url: "http://127.0.0.1:5000/api/link/",
            headers: auth_header,
            method: "delete",
            data: link_details
        }).then(response => {
            if (response.data["message"].includes("Success")) {
                cy.remove(link);
                resolve(true)
            } else {
                alert("Failed to delete node. " + response.data["message"]);
                resolve(false);
            }
        });
    });
}

export function get_metadata(uri, metadata_list, auth_header) {
    return new Promise(function (resolve, reject) {
        axios({
            url: "http://127.0.0.1:5000/api/metadata/" + uri,
            headers: auth_header,
            method: "get"
        }).then(response => {
            let response_data = response["data"].data;
            if (response_data.length != 0) {
                for (let i = 0; i < response_data.length; i++) {
                    metadata_list.push({
                        meta_id: response_data[i]["meta_id"],
                        category: response_data[i]["category"],
                        metadata: response_data[i]["data"]
                    });
                }
            }
            resolve()
        });
    });
}

export function load_view(view_id, types_dict, label_dict,
    relationship_dict, auth_header, cy) {
    return new Promise(function (resolve) {
        const requests = [
            axios({
                url: "http://127.0.0.1:5000/api/node/",
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
            let nodes = values[0].data["data"]
            let links = values[1].data["data"]
            cy.elements().remove()
            let type_count = {}
            for (let i = 0; i < nodes.length; i++) {
                if (nodes[i].view_id == view_id) {
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
                                view_id: view_id,
                                label_id: nodes[i].label_id,
                                label_text: label_dict[nodes[i].label_id],
                                icon: nodes[i].icon
                            },
                            imglink: "https://cors-anywhere.herokuapp.com/" + nodes[i].icon
                        }
                    });
                }
            }

            for (let i = 0; i < links.length; i++) {
                if (links[i].view_id == view_id) {
                    cy.add({
                        group: "edges",
                        data: {
                            id: "l" + links[i].link_id,
                            name: relationship_dict[links[i].relationship_id],
                            source: links[i].node_id_1,
                            target: links[i].node_id_2,
                            payload: {
                                link_id: links[i].link_id,
                                relationship_id: links[i].relationship_id,
                                relationship_message: relationship_dict[links[i].relationship_id],
                                view_id: links[i].view_id
                            }
                        }
                    });
                }
            }
            setTimeout(resolve, 1500)
        })

    });
}