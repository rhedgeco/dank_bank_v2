let group_list = document.getElementById('groups'); //store reference to the list of groups

function getCookie(cname) {
  var name = cname + '=';
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return 0;
}

function init_home() {
  let xhr = new XMLHttpRequest();
  xhr.open('GET', 'api/users?session=' + getCookie('session_id'));
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function () {
    if (xhr.status === 200) {
      var json = JSON.parse(xhr.responseText);
      console.log(json);
      document.getElementById('name').innerText = json['nickname']; //retrieve and display nick name
      let groups = json['groups']; //retreive groups from JSON
      let testGroups = ['roommates', 'work'];

      //go through list of groups and create list elements
      for (var i = 0; i < groups.length; i++) {
        let group = document.createElement('li');
        group.id = Object.keys(groups[i]);
        group.appendChild(document.createTextNode(Object.values(groups[i])[0]));
        group_list.appendChild(group);
      }

      //add event listener to each list element
      for (let i = 0; i < group_list.childElementCount; i++) {
        let list_item = group_list.childNodes[i];

        list_item.addEventListener('click', () => {
          let xhr = new XMLHttpRequest();
          xhr.open(
            'GET',
            'api/groups?session=' +
              getCookie('session_id') +
              '&id=' +
              list_item.id
          );
          xhr.setRequestHeader(
            'Content-Type',
            'application/x-www-form-urlencoded'
          );
          xhr.onload = function () {
            if (xhr.status === 200) {
              console.log('successfully retrieving group');
            }
          };
          xhr.send();
        });
      }
    }
  };
  xhr.send();
}

window.onload = function () {
  init_home();
};
