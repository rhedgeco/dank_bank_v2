var current_user;

//display form
function relocate() {
  let url_string = window.location;
  let url = new URL(url_string);
  let group_id = url.searchParams.get('group_id');
  window.location = 'create_transaction.html?group_id=' + group_id;
}

function retrieve_id(callback) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', 'api/users?session=' + getCookie('session_id'));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
      if (xhr.status === 200) {
        callback(JSON.parse(xhr.responseText));
        resolve('loaded user');
      }
    };
    xhr.send();
  });
}

function init_transaction_form() {
  let url_string = window.location;
  let url = new URL(url_string);
  let group_id = url.searchParams.get('group_id');

  //set up transaction form
  let xhr = new XMLHttpRequest();
  xhr.open(
    'GET',
    'api/groups?session=' + getCookie('session_id') + '&group_id=' + group_id
  );
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = async function () {
    if (xhr.status === 200) {
      let groupInfo = JSON.parse(xhr.responseText);
      let group;
      console.log(groupInfo);
      console.log(Object.keys(groupInfo['users']));

      let id_list = Object.keys(groupInfo['users']);
      let members = Object.values(groupInfo['users']);

      //loop through list of members and display all members other than current user
      for (let i = 0; i < members.length; i++) {
        await retrieve_id((user_data) => {
          if (user_data['id'] !== id_list[i]) {
            let group_members = document.getElementById('member_list');
            let member = document.createElement('li');
            member.classList.add('collection-item');
            member.appendChild(document.createTextNode(members[i]));
            member.id = id_list[i];
            group_members.appendChild(member);
          }
        });
      }

      let group_members = document.getElementById('member_list').children;

      //set element style attribute on click
      for (let i = 0; i < group_members.length; i++) {
        console.log(group_members[i]);
        group_members[i].onclick = function () {
          if (this.style.backgroundColor !== 'rgb(104, 159, 56)') {
            this.style.backgroundColor = '#689f38';
          } else {
            this.removeAttribute('style');
          }
        };
      }
    }
  };
  xhr.send();
}

let btn = document.getElementById('submit_transaction');

//API CALL
btn.addEventListener('click', () => {
  let url_string = window.location;
  let url = new URL(url_string);
  let group_id = url.searchParams.get('group_id');

  //extract form data
  let amount = document.getElementById('paid').value;
  let desc = document.getElementById('desc').value;
  let members = document.getElementById('member_list').children;
  let paid = [];

  for (let i = 0; i < members.length; i++) {
    if (members[i].style.backgroundColor === 'rgb(104, 159, 56)') {
      paid.push(members[i].id);
    }
  }

  console.log(paid);
  console.log(amount);
  console.log(desc);

  // let xhr = new XMLHttpRequest();
  // xhr.open(
  //   'POST',
  //   'api/transactions?session=' +
  //     getCookie('session_id') +
  //     '&group_id=' +
  //     group_id +
  //     '&amount=' + amount
  //     '&paid=' +
  // );
  // xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  // xhr.onload = function () {
  //   if (xhr.status === 200) {
  //     window.location = '/group.html?group_id=' + group_id;
  //   }
  // };
  // xhr.send();
});

$(document).ready(init_transaction_form());
