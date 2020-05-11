from dataclasses import dataclass
from typing import List


@dataclass
class Debt:
    payer_id: int
    #payer: str
    leech_id: int
    #leech: str
    amount: float

debts_list: List[Debt] = []



@dataclass
class Transaction:
    payer_id: int
    #payer: str
    #leech_id:int
    leeches_id: List[int]
    amount: float

    #split_type: str = 'even'




def show_debt_by_id(search_id:int, owed_to_id:int, transaction: List[Transaction]):
    # TODO: take the transactions and output a list of debts
    #debtors_list: List[Debt] = []
    debt = 0
    amt = 0
    for t in transaction:
        if t.payer_id == owed_to_id:    
            for i in t.leeches_id:
                if i == search_id:
                    amt = t.amount/(len(t.leeches_id) + 1)
                    debt += amt
                    #print(owed_to_id," paid ",amt," to ",search_id)
                else:
                    continue
        elif t.payer_id == search_id:
            for i in t.leeches_id:
                if i == owed_to_id:
                    amt = (t.amount/(len(t.leeches_id)+1))
                    debt -= amt
                    #print(search_id," paid ",amt," to ",owed_to_id)
                else:
                    continue       
    #print(search_id,"owes $",debt, "to", owed_to_id)
    if debt >= 0 and search_id != owed_to_id:
        debts_list.append(Debt(owed_to_id, search_id, debt))
        #debts_list = debtors_list.copy()
        
        
        
        
        
        
        
def display_all(members: List[int], transaction: List[Transaction], display:int):
    for i in members:
        for j in members:
            show_debt_by_id(i,j,transaction)
    if display > 0:
        print(*debts_list, sep = "\n")  
                                                




def total_debt_member(member_id:int, members: List[int]):
    total_amt = 0
    for i in members:
        if i == member_id:
            for d in debts_list:
                if d.leech_id == member_id:
                    total_amt += d.amount
                elif d.payer_id == member_id:
                    total_amt -= d.amount
    print(member_id, "owes", total_amt, "in total")
                
    
    
                               
def solve_triangle(i: int, j: int, k: int):
    ij_amt: float
    ki_amt: float
    kj_amt: float
    jk_amt: float
    for d in debts_list:
        if k == d.leech_id and i == d.payer_id and d.amount > -1:
            ki_amt = d.amount
            for e in debts_list:
                if i == e.leech_id and j == e.payer_id and e.amount > -1:
                    ij_amt = e.amount
                    for f in debts_list:
                        if j == f.payer_id and k == f.leech_id:
                            kj_amt = f.amount
                            d.amount = 0
                            e.amount = 0
                            f.amount = ij_amt + ki_amt + kj_amt
                            
                            
                            

def make_transitive(members: List[int]):
   for i in members:
       for j in members:
           for k in members:
               solve_triangle(i,j,k)                            
                            

def one_call(members_list, transaction: List[Transaction]):
    display_all(members_list, transaction,0)
    make_transitive(members_list)
                            
                        
                            
                            


#def transfer_debt_total
members_list: List[int] = [1,2,3,4,5]

# tran1 = Transaction(3,[2,1,4,5],50)
# tran2 = Transaction(1,[2,3,4,5],100)
# tran3 = Transaction(2,[1,3,4,5],100)
# tran4 = Transaction(3,[3,4,5],20)
# tran5 = Transaction(4,[5],50)
# tran6 = Transaction(2,[1],40)
# tran7 = Transaction(5,[3],50)
# tran8 = Transaction(3,[1],80)
#tran9 = Transaction(2,[1,3,4,5],100)

#ransfer_debt_by_id(2,1,[tran1,tran2,tran3])

#print (debts_list)
#print("debts list before transitive using 'display_all' call")

#display_all(members_list,[tran1,tran2,tran3, tran4, tran5, tran6, tran7, tran8])

# total_debt_member(1,members_list)
# total_debt_member(2,members_list)
# total_debt_member(3,members_list)
# total_debt_member(4,members_list)
# total_debt_member(5,members_list)

#print("length of debt list: ",len(debts_list))
#make_transitive(members_list)


#make_transitive(members_list)

#print(*debts_list, sep = "\n") 
#print("length of debt list: ",len(debts_list))                                              
# total_debt_member(1,members_list)
# total_debt_member(2,members_list)
# total_debt_member(3,members_list)
# total_debt_member(4,members_list)
# total_debt_member(5,members_list)

#display_all(members_list,[tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8],1)
#make_transitive(members_list)

#one_call(members_list, [tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8])
# print("length of debt list: ",len(debts_list))
# print(*debts_list, sep = "\n") 





# # display_all(members_list, [tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8])
# # make_transitive(members_list)
# # print("length of debt list: ",len(debts_list))

# one_call(members_list, [tran1,tran8, tran2,tran3, tran4, tran7, tran5, tran6, tran7, tran8])
# # print(*debts_list, sep = "\n") 


# print("length of debt list: ",len(debts_list))
# print(*debts_list, sep = "\n") 
