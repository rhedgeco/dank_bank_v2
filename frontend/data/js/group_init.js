import { loadUser, getCookie, configureGroups } from './load_user.js';
var groupID;

function loadGroup() {
  if (!groupID) {
    var url_string = window.location;
    var url = new URL(url_string);
    var id = url.searchParams.get('group_id');
    groupID = id;
  }

  let xhr = new XMLHttpRequest();
  xhr.open(
    'GET',
    'api/groups?session=' + getCookie('session_id') + '&group_id=' + groupID
  );

  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function () {
    if (xhr.status === 200) {
      var groupInfo = JSON.parse(xhr.responseText);
      console.log(groupInfo);
      document.getElementById('group_header').innerText =
        groupInfo['group_name'];

      if (groupInfo['users'].length < 2) {
        document.getElementById('group_count').innerText =
          groupInfo['users'].length + ' member';
      } else {
        document.getElementById('group_count').innerText =
          groupInfo['users'].length + ' member';
      }

      let debtList = document.getElementById('debtList');
      let debts = groupInfo['debts'];
      console.log(debts);

      for (let i = 0; i < 1; i++) {
        let debt = document.createElement('li');
        let who = document.createElement('p');
        let settleBtn = document.createElement('button');
        let amount = document.createElement('p');

        who.appendChild(document.createTextNode('danny'));
        amount.appendChild(document.createTextNode('$100'));
        settleBtn.appendChild(document.createTextNode('Settle'));
        debt.appendChild(who);
        debt.appendChild(settleBtn);
        debt.appendChild(amount);
        debtList.appendChild(debt);
      }
    }
  };
  xhr.send();
}

export function setGroupID(id) {
  group.id = id;
  console.log(group.id);
}

window.onload = async function () {
  let user = await loadUser();
  configureGroups();
  loadGroup();
};

export { groupID };
