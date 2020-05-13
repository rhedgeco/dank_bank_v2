import { loadUser, getCookie, configureGroups } from './load_user.js';

function loadGroup() {
  var url_string = window.location;
  var url = new URL(url_string);
  var id = url.searchParams.get('group_id');
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
      document.getElementById('groupName').innerText = groupInfo['group_name'];

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
        let debtItem = document.createElement('li');
        let debt = document.createElement('p');
        let amount = document.createElement('p');
        let arrow = document.createElement('i');

        arrow.classList.add('material-icons');
        arrow.appendChild(document.createTextNode('arrow_forward'));

        debt.appendChild(document.createTextNode('Danny '));
        debt.appendChild(arrow);
        debt.appendChild(document.createTextNode(' Ryan'));
        amount.appendChild(document.createTextNode('$100'));

        // let settleBtn = document.createElement('button');
        // settleBtn.appendChild(document.createTextNode('Settle'));
        // debt.appendChild(who);
        // debt.appendChild(settleBtn);
        debtItem.appendChild(debt);
        debtItem.appendChild(amount);
        debtList.appendChild(debtItem);
      }
    }
  };
  xhr.send();
}

<<<<<<< HEAD
window.onload = async function () {
  this.console.log('relaoding');
=======
async function init_group() {
>>>>>>> master
  let user = await loadUser();
  configureGroups();
  loadGroup();
}

$(document).ready(init_group());