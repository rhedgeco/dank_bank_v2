function goto_group_page(group_id) {
    window.location = 'group.html?group_id=' + group_id;
}

function populate_photos(photos, photo) {
    for (let i = 0; i < photos.length; i++) {
        photos[i].src = photo;
    }
}

function populate_names(names, name) {
    for (let i = 0; i < names.length; i++) {
        names[i].innerText = name;
    }
}

function populate_groups(group_list, groups) {
    //go through list of groups and create list elements
    for (let i = 0; i < groups.length; i++) {
        let group = document.createElement('li');
        group.id = Object.keys(groups[i]); //set id to the same group id from the db
        group.appendChild(document.createTextNode(Object.values(groups[i])[0])); //get group name from the object
        group_list.appendChild(group);
        group.onclick = function () {
            goto_group_page(this.id);
        }
    }
}

function init_navigation() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', 'api/users?session=' + getCookie('session_id'));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status !== 200) {
            window.location = '/';
        } else {
            let json = JSON.parse(xhr.responseText);
            let names = document.getElementsByClassName('user-name');
            let photos = document.getElementsByClassName('login-photo');
            let group_list = document.getElementById('groups'); //store reference to the list of groups
            populate_names(names, json['nickname']);
            populate_photos(photos, json['photo']);
            populate_groups(group_list, json['groups'])

        }
    };
    xhr.send();
}


function sign_out() {
    document.cookie = 'session_id=0';
    window.location = '/';
}

$(document).ready(init_navigation());
