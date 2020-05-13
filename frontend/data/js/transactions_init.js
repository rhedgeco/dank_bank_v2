function load_trans() {
    let url_string = window.location;
    let url = new URL(url_string);
    let id = url.searchParams.get('group_id');

    document.getElementById("view_group").onclick = function () {
        window.location = '/group.html?group_id=' + id;
    };

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
            document.getElementById('group_title').innerText = groupInfo['group_name'];

            let members = groupInfo['users'];
            let trans_list = document.getElementById('trans_list');
            let trans = groupInfo['transactions'];
            console.log(trans);

            for (let i = 0; i < trans.length; i++) {
                let debtItem = document.createElement('li');
                let debt = document.createElement('p');
                let amount = document.createElement('p');
                let arrow = document.createElement('i');

                arrow.classList.add('material-icons');
                arrow.appendChild(document.createTextNode('arrow_forward'));

                debt.appendChild(document.createTextNode(members[trans[i]['user_pay']]));
                debt.appendChild(document.createTextNode(' paid for '));
                debt.appendChild(document.createTextNode(trans[i]['description']));
                amount.appendChild(document.createTextNode('$' + trans[i]['amount']));

                debtItem.appendChild(debt);
                debtItem.appendChild(amount);
                trans_list.appendChild(debtItem);

                debtItem.classList.add("waves-effect");
                debtItem.classList.add("waves-light");
                debtItem.onclick = function () {
                    window.location = '/inspect_transaction.html?trans_id=' + trans[i]['trans_id'];
                }
            }
        }
    };
    xhr.send();
}

$(document).ready(load_trans());