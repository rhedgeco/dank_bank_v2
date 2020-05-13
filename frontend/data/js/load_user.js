export function getCookie(cname) {
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

export function configureGroups() {
  console.log('confirguring groups');
  let group_list = document.getElementById('groups'); //store reference to the list of groups
  //add event listener to each group on the list
  for (let i = 0; i < group_list.childElementCount; i++) {
    let list_item = group_list.childNodes[i];

    list_item.addEventListener('click', () => {
      window.location = 'group.html?group_id=' + list_item.id;
    });
  }
}

export function loadUser() {
  console.log('this is loaduser()');

  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', 'api/users?session=' + getCookie('session_id'));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
      if (xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        console.log(json);
        let group_list = document.getElementById('groups'); //store reference to the list of groups
        document.getElementById('name').innerText = json['nickname']; //retrieve and display nick name
        resolve('loaded user');
      }
    };
    xhr.send();
  });
}
