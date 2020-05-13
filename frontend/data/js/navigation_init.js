function goto_group_page(group_id) {
    window.location = 'group.html?group_id=' + group_id;
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
            document.getElementById('name').innerText = json['nickname']; //retrieve and display nick name
            document.getElementById('photo').src = json['photo'];
            let groups = json['groups'];
            //go through list of groups and create list elements
            let group_list = document.getElementById('groups'); //store reference to the list of groups
            for (var i = 0; i < groups.length; i++) {
                let group = document.createElement('li');
                group.id = Object.keys(groups[i]); //set id to the same group id from the db
                group.appendChild(document.createTextNode(Object.values(groups[i])[0])); //get group name from the object
                group_list.appendChild(group);
                group.onclick = function () {
                    goto_group_page(this.id);
                }
            }
        }
    };
    xhr.send();
}

window.onload = function () {
    init_navigation();
};

function sign_out() {
    document.cookie = 'session_id=0';
    window.location = '/';
}