candidate_list = []
candidate_dics = {}
grafik = {}


def addingUsers():
    while True:
        candidate = input("Podaj uczestnika: ")
        if candidate == 'q':
            break
        candidate_list.append(candidate)
    return candidate_list


def addingPosibilties():
    for candidate in candidate_list:
        days = input(f"Podaj dni w których {candidate} ma pracować (rozdziel przecinkiem bez spacji): ")
        days_list = days.split(',')
        candidate_dics[candidate] = days_list
    return candidate_dics


def assigning():
    week_days = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
    total_days_per_candidate = {candidate: len(days) for candidate, days in candidate_dics.items()}
    
    sorted_candidates = sorted(candidate_dics.keys(), key=lambda c: total_days_per_candidate[c])
    assigned_days_per_candidate = {candidate: 0 for candidate in candidate_dics}
    for day in week_days:
        grafik[day] = []
        for candidate in sorted_candidates:
            if day in candidate_dics[candidate] and len(grafik[day]) < 2 and total_days_per_candidate[candidate] > 0:
                grafik[day].append(candidate)
                total_days_per_candidate[candidate] -= 1
                assigned_days_per_candidate[candidate] += 1
    for candidate, days in assigned_days_per_candidate.items():
        print(f"{candidate}: {days} dni pracy")
        
    return grafik
         

def main():
    addingUsers()
    print(candidate_list)
    addingPosibilties()
    print(candidate_dics)
    assigning()
    print(grafik)
    
main()