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
            console.log(groupInfo);
            console.log(Object.keys(groupInfo['users']));

            let id_list = Object.keys(groupInfo['users']);
            let members = Object.values(groupInfo['users']);

            //loop through list of members and display all members other than current user
            for (let i = 0; i < members.length; i++) {
                let group_members = document.getElementById('member_list');
                let member = document.createElement('li');
                member.classList.add('collection-item');
                member.appendChild(document.createTextNode(members[i]));
                member.id = id_list[i];
                group_members.appendChild(member);
            }

            let group_members = document.getElementById('member_list').children;

            //set element style attribute on click
            for (let i = 0; i < group_members.length; i++) {
                console.log(group_members[i]);
                group_members[i].onclick = function () {
                    if (this.classList.contains('selected'))
                        this.classList.remove('selected');
                    else this.classList.add('selected');
                };
            }
        }
    };
    xhr.send();
}

function submit_form() {
    let url_string = window.location;
    let url = new URL(url_string);
    let group_id = url.searchParams.get('group_id');

    let amount = document.getElementById('paid').value;
    let desc = document.getElementById('desc').value;

    let dlist = document.getElementById('member_list').childNodes;
    let debtors = '';
    for (let i = 1; i < dlist.length; i++) {
        if (dlist[i].classList.contains('selected'))
            debtors = debtors + dlist[i].id + ',';
    }
    debtors = debtors.substring(0, debtors.length - 1);
    console.log(debtors);

    let xhr = new XMLHttpRequest();
    xhr.open(
        'POST',
        'api/transactions?session=' +
        getCookie('session_id') +
        '&group_id=' +
        group_id +
        '&amount=' +
        amount +
        '&paid=' +
        debtors +
        '&description=' +
        desc
    );
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            window.location = '/group.html?group_id=' + group_id;
        }
    };
    xhr.send();
}

function goBack() {
    window.history.back();
}

$(document).ready(init_transaction_form());
