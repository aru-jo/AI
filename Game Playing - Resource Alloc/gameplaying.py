
DAYS_IN_WEEK = 7
WEEKLY_STRING_INDEX = 4
PICK_MARKER = 3
CHECKER_INDEX = 1
DATE_START_INDEX = 13
DATE_END_INDEX = 20


class Solver:
    def __init__(self, w_spaces, w_beds):
        self.w_spaces = w_spaces
        self.w_beds = w_beds

    def get_next_state(self, this_applicant, organization):
        lahsa_pattern = list(self.w_beds)
        spla_pattern = list(self.w_spaces)
        if organization:
            for iterator in range(DAYS_IN_WEEK):
                spla_pattern[iterator] += int(this_applicant[WEEKLY_STRING_INDEX][iterator])
        else:
            for iterator in range(DAYS_IN_WEEK):
                lahsa_pattern[iterator] += int(this_applicant[WEEKLY_STRING_INDEX][iterator])
        return Solver(spla_pattern, lahsa_pattern)

    def check_if_full(self, this_applicant, to_play):
        if to_play:
            for iterator in range(DAYS_IN_WEEK):
                if (self.w_spaces[iterator] + int(this_applicant[WEEKLY_STRING_INDEX][iterator])) > p:
                    return False
        else:
            for iterator in range(DAYS_IN_WEEK):
                if (self.w_beds[iterator] + int(this_applicant[WEEKLY_STRING_INDEX][iterator])) > b:
                    return False
        return True

    def return_efficiency(self):
        spla_efficiency = sum(int(iterator) for iterator in self.w_spaces) / float(p * DAYS_IN_WEEK)
        lahsa_efficiency = sum(int(iterator) for iterator in self.w_beds) / float(b * DAYS_IN_WEEK)
        return lahsa_efficiency, spla_efficiency

    def negate(self, to_play):
        spla_total_score = list(self.w_spaces)
        lahsa_total_score = list(self.w_beds)
        if to_play:
            for single_applicant in total_applicants:
                if single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'S':
                    if single_applicant[CHECKER_INDEX] == 'O':
                        for iterator in range(DAYS_IN_WEEK):
                            if spla_total_score[iterator] + int(single_applicant[WEEKLY_STRING_INDEX][iterator]) > p:
                                return -1, -1
                        for iterator in range(DAYS_IN_WEEK):
                            spla_total_score[iterator] += int(single_applicant[WEEKLY_STRING_INDEX][iterator])
        else:
            for single_applicant in total_applicants:
                if single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'L':
                    if single_applicant[CHECKER_INDEX] == 'O':
                        for iterator in range(DAYS_IN_WEEK):
                            if lahsa_total_score[iterator] + int(single_applicant[WEEKLY_STRING_INDEX][iterator]) > b:
                                return -1, -1
                        for iterator in range(DAYS_IN_WEEK):
                            lahsa_total_score[iterator] += int(single_applicant[WEEKLY_STRING_INDEX][iterator])
        return sum(lahsa_total_score) / float(b * DAYS_IN_WEEK), sum(spla_total_score) / float(p * DAYS_IN_WEEK)


tuple_dict = {}

input_pointer = [input_line.rstrip('\n\r') for input_line in open('input.txt')]


def lahsa_maximiser(solver_object, spla_moves, lahsa_moves):
    identifier = False
    s_best = 0
    l_best = float('-inf')
    pruning_lahsa = {}
    spla_tuple = tuple(sorted(spla_moves))
    lahsa_tuple = tuple(sorted(lahsa_moves))
    list_dict = tuple_dict.get((spla_tuple, lahsa_tuple))
    if list_dict is not None:
        return list_dict[1], list_dict[0]
    for single_applicant in total_applicants:
        if (single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'L') and 'O' == \
                single_applicant[CHECKER_INDEX]:
            if solver_object.check_if_full(single_applicant, 0):
                if pruning_lahsa.get(single_applicant[4]) is not None:
                    continue
                else:
                    pruning_lahsa[single_applicant[4]] = single_applicant[0]
                single_applicant[CHECKER_INDEX] = 'L'
                lahsa_moves.append(single_applicant[0])
                next_state = solver_object.get_next_state(single_applicant, 0)
                s_l, s_s = spla_maximiser(next_state, spla_moves, lahsa_moves)
                if s_l > l_best:
                    l_best = s_l
                    s_best = s_s
                single_applicant[CHECKER_INDEX] = 'O'
                lahsa_moves.pop()
                identifier = True
                if l_best == 1:
                    return l_best, s_best
    if identifier:
        tuple_dict[(spla_tuple, lahsa_tuple)] = [s_best, l_best]
    else:
        return lonely_spla(solver_object, spla_moves, lahsa_moves)
    return l_best, s_best


def spla_maximiser(solver_object, spla_moves, lahsa_moves):
    identifier = False
    b_s = float('-inf')
    b_l = 0
    lahsa_tuple = tuple(sorted(lahsa_moves))
    spla_tuple = tuple(sorted(spla_moves))
    pruning_spla = {}
    list_dict = tuple_dict.get((spla_tuple, lahsa_tuple))
    if list_dict is not None:
        return list_dict[1], list_dict[0]
    for single_applicant in total_applicants:
        if not (not (single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'S') or not (
                single_applicant[CHECKER_INDEX] == 'O')):
            if solver_object.check_if_full(single_applicant, 1):
                if pruning_spla.get(single_applicant[4]) is not None:
                    continue
                else:
                    pruning_spla[single_applicant[4]] = single_applicant[0]
                single_applicant[CHECKER_INDEX] = 'S'
                spla_moves.append(single_applicant[0])
                next_state = solver_object.get_next_state(single_applicant, 1)
                s_l, s_s = lahsa_maximiser(next_state, spla_moves, lahsa_moves)
                if s_s > b_s:
                    b_l = s_l
                    b_s = s_s
                single_applicant[CHECKER_INDEX] = 'O'
                spla_moves.pop()
                identifier = True
                if b_s == 1:
                    return b_l, b_s
    if identifier:
        tuple_dict[(spla_tuple, lahsa_tuple)] = [b_s, b_l]
    else:
        return lonely_lahsa(solver_object, spla_moves, lahsa_moves)
    return b_l, b_s


def lonely_spla(solver_object, spla_moves, lahsa_moves):
    identifier = False
    s_l, s_s = solver_object.negate(1)
    if s_s is not -1:
        return s_l, s_s
    best_spla = float('-inf')
    best_lahsa = 0
    pruning_l_spla = {}
    tuple_spla = tuple(sorted(spla_moves))
    tuple_lahsa = tuple(sorted(lahsa_moves))
    list_dict = tuple_dict.get((tuple_spla, tuple_lahsa))
    if list_dict is not None:
        return list_dict[1], list_dict[0]
    for single_applicant in total_applicants:
        if not (not (single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'S') or not (
                single_applicant[CHECKER_INDEX] == 'O') or not solver_object.check_if_full(single_applicant, 1)):
            if pruning_l_spla.get(single_applicant[4]) is not None:
                continue
            else:
                pruning_l_spla[single_applicant[4]] = single_applicant[0]
            single_applicant[CHECKER_INDEX] = 'S'
            spla_moves.append(single_applicant[0])
            next_state = solver_object.get_next_state(single_applicant, 1)
            s_l, s_s = lonely_spla(next_state, spla_moves, lahsa_moves)
            if s_s > best_spla:
                best_spla = s_s
                best_lahsa = s_l
            single_applicant[CHECKER_INDEX] = 'O'
            spla_moves.pop()
            identifier = True
            if best_spla == 1:
                return best_lahsa, best_spla
    if identifier:
        tuple_dict[(tuple_spla, tuple_lahsa)] = [best_spla, best_lahsa]
    else:
        return solver_object.return_efficiency()
    return best_lahsa, best_spla


def lonely_lahsa(solver_object, spla_moves, lahsa_moves):
    s_l, s_s = solver_object.negate(0)
    if s_l is not -1:
        return s_l, s_s
    identifier = False
    pruning_l_lahsa = {}
    best_spla = 0
    best_lahsa = float('-inf')
    tuple_spla = tuple(sorted(spla_moves))
    tuple_lahsa = tuple(sorted(lahsa_moves))
    list_dict = tuple_dict.get((tuple_spla, tuple_lahsa))
    if list_dict is not None:
        return list_dict[1], list_dict[0]
    for single_applicant in total_applicants:
        if not (not (single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'L') or not (
                single_applicant[CHECKER_INDEX] == 'O') or not solver_object.check_if_full(single_applicant, 0)):
            if pruning_l_lahsa.get(single_applicant[4]) is not None:
                continue
            else:
                pruning_l_lahsa[single_applicant[4]] = single_applicant[0]
            single_applicant[CHECKER_INDEX] = 'L'
            lahsa_moves.append(single_applicant[0])
            next_state = solver_object.get_next_state(single_applicant, 0)
            s_l, s_s = lonely_lahsa(next_state, spla_moves, lahsa_moves)
            if s_l > best_lahsa:
                best_lahsa = s_l
                best_spla = s_s
            single_applicant[CHECKER_INDEX] = 'O'
            lahsa_moves.pop()
            identifier = True
            if best_lahsa == 1:
                return best_lahsa, best_spla
    if identifier:
        tuple_dict[(tuple_spla, tuple_lahsa)] = [best_spla, best_lahsa]
    else:
        return solver_object.return_efficiency()
    return best_lahsa, best_spla


b = int(input_pointer[0])
p = int(input_pointer[1])

_l = int(input_pointer[2])  # No of people shelter has already picked
s = int(input_pointer[_l + 3])  # No of people parking has already picked

a = int(input_pointer[s + _l + 4])  # Total no of applicants

l_sa = []

for iterator in range(3, _l + 3):
    l_sa.append(input_pointer[iterator])  # Add people who're already picked to set by shelter

s_sa = []

for iterator in range(_l + 4, s + _l + 4):
    s_sa.append(input_pointer[iterator])  # Add people who're already picked to set by spaces

total_applicants = []

parking_weekly = [0] * 7
beds_weekly = [0] * 7


for iterator in range(s + _l + 5, s + _l + a + 5):
    single_app = str(input_pointer[iterator])
    if single_app[0:5] in l_sa:
        for day in range(DATE_START_INDEX, DATE_END_INDEX):
            beds_weekly[day - DATE_START_INDEX] += int(single_app[day])
        continue
    if single_app[0:5] in s_sa:
        for day in range(DATE_START_INDEX, DATE_END_INDEX):
            parking_weekly[day - DATE_START_INDEX] += int(single_app[day])
        continue

    if single_app[10] == 'N' and single_app[11] == 'Y' and single_app[12] == 'Y' and single_app[5] == 'F' and int(
            single_app[6:9]) > 17 and single_app[9] == 'N':
        total_applicants.append([single_app[0:5], 'O', sum(int(i) for i in single_app[DATE_START_INDEX:DATE_END_INDEX]), 'C', single_app[DATE_START_INDEX:DATE_END_INDEX]])
    else:
        if single_app[10] == 'N' and single_app[11] == 'Y' and single_app[12] == 'Y':
            total_applicants.append([single_app[0:5], 'O', sum(int(i) for i in single_app[DATE_START_INDEX:DATE_END_INDEX]), 'S', single_app[DATE_START_INDEX:DATE_END_INDEX]])
        elif single_app[5] == 'F' and int(single_app[6:9]) > 17 and single_app[9] == 'N':
            total_applicants.append([single_app[0:5], 'O', sum(int(i) for i in single_app[DATE_START_INDEX:DATE_END_INDEX]), 'L', single_app[DATE_START_INDEX:DATE_END_INDEX]])

total_applicants.sort()

solver_obj = Solver(parking_weekly, beds_weekly)

max_outcome_spla = 0

l_moves = []
s_moves = []

best_s_s = float('-inf')
s_l = float('-inf')

prune = {}

for single_applicant in total_applicants:
    if (single_applicant[PICK_MARKER] == 'C' or single_applicant[PICK_MARKER] == 'S') and solver_obj.check_if_full(single_applicant, 1):
        if prune.get(single_applicant[4]) is not None:
            continue
        else:
            prune[single_applicant[4]] = single_applicant[0]
        single_applicant[CHECKER_INDEX] = 'S'
        next_state = solver_obj.get_next_state(single_applicant, 1)
        s_moves.append(single_applicant[0])
        score_lahsa, score_spla = lahsa_maximiser(next_state, s_moves, l_moves)
        if score_spla > best_s_s:
            max_outcome_spla = single_applicant[0]
            best_s_s = score_spla
            s_l = score_lahsa
        single_applicant[CHECKER_INDEX] = 'O'
        s_moves.pop()
        if best_s_s == 1:
            break

with open("output.txt", "w+") as output:
    output.write(max_outcome_spla)





























