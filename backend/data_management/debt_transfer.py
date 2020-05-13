from dataclasses import dataclass
from typing import List


@dataclass
class Debt:
    receiver: str
    sender: str
    amount: float


@dataclass
class Transaction:
    payer_id: str
    leeches_id: List[str]
    amount: float

    split_type: str = 'even'


def transactions_to_debt(trans: List[Transaction]):
    debts: List[Debt] = []

    def add_trans_to_debts(amount: float, send: str, receive: str):
        for d in debts:
            if send == receive:
                break
            elif d.sender == send and d.receiver == receive:  # if there is an existing debt to add to
                d.amount += amount
                break
            elif d.sender == receive:
                d.amount = d.amount - amount
                if d.amount >= 0:
                    add_trans_to_debts(amount, send, d.receiver)
                else:
                    debts.remove(d)
                    if d.amount < 0:
                        add_trans_to_debts(-d.amount, send, receive)
                    add_trans_to_debts(amount + d.amount, send, d.receiver)
                break
            elif d.receiver == send:
                d.amount = d.amount - amount
                if d.amount >= 0:
                    add_trans_to_debts(amount, d.sender, receive)
                else:
                    debts.remove(d)
                    if d.amount < 0:
                        add_trans_to_debts(amount + d.amount, d.sender, receive)
                    add_trans_to_debts(-d.amount, send, receive)
                break
        else:
            debts.append(Debt(receive, send, amount))

    for t in trans:
        for l in t.leeches_id:
            add_trans_to_debts(
                amount=(int(float(t.amount) * 100) // int(len(t.leeches_id))) / 100,
                send=l,
                receive=t.payer_id
            )

    return debts


if __name__ == '__main__':
    transactions = [
        Transaction('0', ['0', '1', '2', '3'], 60),
        Transaction('4', ['0', '4'], 90)
    ]
    print(transactions_to_debt(transactions))

#
# class TransitiveDebt:
#
#     def __init__(self):
#         self._debts_list: List[Debt] = []
#
#     def _show_debt_by_id(self, search_id: str, owed_to_id: str, transaction: List[Transaction]):
#         # TODO: take the transactions and output a list of debts
#         # debtors_list: List[Debt] = []
#         debt = 0
#         amt = 0
#         for t in transaction:
#             if t.payer_id == owed_to_id:
#                 for i in t.leeches_id:
#                     if i == search_id:
#                         amt = float(t.amount) / int((len(t.leeches_id) + 1))
#                         debt += amt
#                         # print(owed_to_id," paid ",amt," to ",search_id)
#                     else:
#                         continue
#             elif t.payer_id == search_id:
#                 for i in t.leeches_id:
#                     if i == owed_to_id:
#                         amt = float(t.amount) / int((len(t.leeches_id) + 1))
#                         debt -= amt
#                         # print(search_id," paid ",amt," to ",owed_to_id)
#                     else:
#                         continue
#                         # print(search_id,"owes $",debt, "to", owed_to_id)
#         if debt >= 0 and search_id != owed_to_id:
#             self._debts_list.append(Debt(owed_to_id, search_id, debt))
#             # debts_list = debtors_list.copy()
#
#     def _display_all(self, members: List[str], transaction: List[Transaction], display: int):
#         for i in members:
#             for j in members:
#                 self._show_debt_by_id(i, j, transaction)
#         if display > 0:
#             print(*self._debts_list, sep="\n")
#
#     def _total_debt_member(self, member_id: str, members: List[str]):
#         total_amt = 0
#         for i in members:
#             if i == member_id:
#                 for d in self._debts_list:
#                     if d.sender == member_id:
#                         total_amt += d.amount
#                     elif d.receiver == member_id:
#                         total_amt -= d.amount
#         print(member_id, "owes", total_amt, "in total")
#
#     def _solve_triangle(self, i: str, j: str, k: str):
#         ij_amt: float
#         ki_amt: float
#         kj_amt: float
#         jk_amt: float
#         for d in self._debts_list:
#             if k == d.sender and i == d.receiver and d.amount > -1:
#                 ki_amt = d.amount
#                 for e in self._debts_list:
#                     if i == e.sender and j == e.receiver and e.amount > -1:
#                         ij_amt = e.amount
#                         for f in self._debts_list:
#                             if j == f.receiver and k == f.sender:
#                                 kj_amt = f.amount
#                                 d.amount = 0
#                                 e.amount = 0
#                                 f.amount = ij_amt + ki_amt + kj_amt
#
#     def _make_transitive(self, members: List[str]):
#         for i in members:
#             for j in members:
#                 for k in members:
#                     self._solve_triangle(i, j, k)
#
#     def one_call(self, transaction: List[Transaction]):
#
#         members_list = []
#         for trans in transaction:
#             for member in trans.leeches_id:
#                 if member not in members_list:
#                     members_list.append(member)
#
#         self._display_all(members_list, transaction, 0)
#         self._make_transitive(members_list)
#         return self._debts_list
#
# # def transfer_debt_total
# # members_list: List[str] = [1, 2, 3, 4, 5]
#
# # tran1 = Transaction(3,[2,1,4,5],50)
# # tran2 = Transaction(1,[2,3,4,5],100)
# # tran3 = Transaction(2,[1,3,4,5],100)
# # tran4 = Transaction(3,[3,4,5],20)
# # tran5 = Transaction(4,[5],50)
# # tran6 = Transaction(2,[1],40)
# # tran7 = Transaction(5,[3],50)
# # tran8 = Transaction(3,[1],80)
# # tran9 = Transaction(2,[1,3,4,5],100)
#
# # ransfer_debt_by_id(2,1,[tran1,tran2,tran3])
#
# # print (debts_list)
# # print("debts list before transitive using 'display_all' call")
#
# # display_all(members_list,[tran1,tran2,tran3, tran4, tran5, tran6, tran7, tran8])
#
# # total_debt_member(1,members_list)
# # total_debt_member(2,members_list)
# # total_debt_member(3,members_list)
# # total_debt_member(4,members_list)
# # total_debt_member(5,members_list)
#
# # print("length of debt list: ",len(debts_list))
# # make_transitive(members_list)
#
#
# # make_transitive(members_list)
#
# # print(*debts_list, sep = "\n")
# # print("length of debt list: ",len(debts_list))
# # total_debt_member(1,members_list)
# # total_debt_member(2,members_list)
# # total_debt_member(3,members_list)
# # total_debt_member(4,members_list)
# # total_debt_member(5,members_list)
#
# # display_all(members_list,[tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8],1)
# # make_transitive(members_list)
#
# # one_call(members_list, [tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8])
# # print("length of debt list: ",len(debts_list))
# # print(*debts_list, sep = "\n")
#
#
# # # display_all(members_list, [tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8])
# # # make_transitive(members_list)
# # # print("length of debt list: ",len(debts_list))
#
# # one_call(members_list, [tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8])
# # # print(*debts_list, sep = "\n")
#
#
# # print("length of debt list: ",len(debts_list))
# # print(*debts_list, sep = "\n")
