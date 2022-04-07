contributers, projects = map(int, input().split())
skills = dict()  # {skill_name: [[list_of_people_at_skill_level] for i in range(11)]}
people = dict()  # {person_name: {...{skill_name: skill_level}, available: boolean}}
waiting = []     # list of projects that have not been completed
in_progress = [] # list of projects that are in progress (project_name, [list of workers], end_day, [(person_name, skill)])
completed = []   # list of completed projects (project_name, [list of workers])

for _ in range(contributers):
    person_name, num_skills = input().split()
    num_skills = int(num_skills)
    people[person_name] = {"available": True}
    for _ in range(num_skills):
        skill_name, skill_level = input().split()
        skill_level = int(skill_level)
        if skill_name not in skills:
            skills[skill_name] = [[] for _ in range(11)]
        skills[skill_name][skill_level].append(person_name)
        people[person_name][skill_name] = skill_level
        
for _ in range(projects):
    project_name, duration, score, deadline, num_roles = input().split()
    duration, score, deadline, num_roles = int(duration), int(score), int(deadline), int(num_roles)
    roles = []
    for _ in range(num_roles):
        skill_name, required_level = input().split()
        required_level = int(required_level)
        roles.append((skill_name, required_level))
    waiting.append((project_name, duration, score, deadline, roles))
    

def in_progress_to_completed(projects_to_remove):

    new_completed = []
    
    def filter_projects(project):
        if project in projects_to_remove:
            completed_project = (project[0], project[1])
            new_completed.append(completed_project)
            for worker in project[1]:
                people[worker]['available'] = True
            return False
        return True

    global in_progress
    in_progress = list(filter(filter_projects, in_progress))
    for new_completed_project in new_completed:
        completed.append(new_completed_project)

# returns list of people or False
def take_project_possible(project, cur_day): 
    p = list()
    mentees = []
  
    lookup = dict() # {skill_name: highest_of_skill_on_team}
    for role in project[4]: 
        found_role = False
        if role[0] in lookup and lookup[role[0]] >= role[1]: # mentor exists
            for cand in skills[role[0]][role[1]-1]:
                if people[cand]['available'] is True: 
                    mentees.append((cand, role[0]))
                    p.append(cand)
                    found_role = True
                    for key in people[cand]:
                        if key != "available" and (key not in lookup or lookup[key] < people[cand][key]):
                            lookup[role[0]] = people[cand][key]

        for level in range(role[1], 11):
            for cand in skills[role[0]][level]:
                if people[cand]['available'] is True: 
                    p.append(cand)
                    found_role = True
                    for key in people[cand]:
                        if key != "available" and (key not in lookup or lookup[key] < people[cand][key]):
                            lookup[role[0]] = people[cand][key]
                            
        if found_role is False: 
            return False

    end_day = cur_day + project[1]
    return (project[0], p, end_day, mentees)


# (project_name, [list of workers], end_day, [(person_name, skill)
def take_project(project):
    
    in_progress.append(project)
    
    project_name = project[0]
    low = project[1]

    def not_target_project(proj):
        if proj[0] == project_name:
            return False 
        return True 

    global waiting
    waiting = list(filter(not_target_project, waiting))

    for name in low:
        people[name]['available'] = False

    mentees = project[3]
    for mentee in mentees:
        people[mentee[0]][mentee[1]] = people.get(people[mentee[0]][mentee[1]], 0) + 1
    

for cur_day in range(200000):
    projects_to_remove = []
    for project in in_progress:
        if project[2] == cur_day:
            projects_to_remove.append(project)
    in_progress_to_completed(projects_to_remove)
    cur_project_index = 0
    while cur_project_index != len(waiting):
        if take_project_possible(waiting[cur_project_index], cur_day):
            take_project(take_project_possible(waiting[cur_project_index], cur_day))
            cur_project_index = 0
        else:
            cur_project_index += 1

print(len(completed))
for result in completed:
    print(result[0])
    print(*result[1])