import { loadUser, getCookie, configureGroups } from './load_user.js';

function loadGroup() {
  let url_string = window.location;
  let url = new URL(url_string);
  let id = url.searchParams.get('group_id');
  console.log(id);

  let xhr = new XMLHttpRequest();
  xhr.open(
    'GET',
    'api/groups?session=' + getCookie('session_id') + '&group_id=' + id
  );

  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function () {
    if (xhr.status === 200) {
      var groupInfo = JSON.parse(xhr.responseText);
      console.log(groupInfo);
      console.log(Object.keys(groupInfo['users']));
      document.getElementById('groupName').innerText = groupInfo['group_name'];
      document.getElementById('groupID').innerHTML = id;

      if (Object.keys(groupInfo['users']).length < 2) {
        document.getElementById('group_count').innerText =
          Object.keys(groupInfo['users']).length + ' member';
      } else {
        document.getElementById('group_count').innerText =
          Object.keys(groupInfo['users']).length + ' members';
      }

      let members = groupInfo['users'];
      let debtList = document.getElementById('debtList');
      let debts = groupInfo['debts'];
      console.log(members);

      for (let i = 0; i < debts.length; i++) {
        let debtItem = document.createElement('li');
        let debt = document.createElement('p');
        let amount = document.createElement('p');
        let arrow = document.createElement('i');

        arrow.classList.add('material-icons');
        arrow.appendChild(document.createTextNode('arrow_forward'));

        debt.appendChild(
          document.createTextNode(members[debts[i]['from']] + ' ')
        );
        debt.appendChild(arrow);
        debt.appendChild(
          document.createTextNode(' ' + members[debts[i]['to']])
        );
        amount.appendChild(document.createTextNode('$' + debts[i]['amount']));

        debtItem.appendChild(debt);
        debtItem.appendChild(amount);
        debtList.appendChild(debtItem);
      }
    }
  };
  xhr.send();
}

function enable_view_transactions() {
  let view_trans = document.getElementById('view_trans');
  view_trans.onclick = function () {
    let url_string = window.location;
    let url = new URL(url_string);
    let id = url.searchParams.get('group_id');
    window.location = '/view_transactions.html?group_id=' + id;
  };
}

async function init_group() {
  let user = await loadUser();
  configureGroups();
  loadGroup();
  enable_view_transactions();
}

$(document).ready(init_group());
