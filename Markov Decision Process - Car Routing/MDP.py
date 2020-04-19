import numpy as np
import time 

gamma = 0.9
cr_p = 0.7
diff_p = 0.1
error = 0.1
error_rate = error*(1-gamma)/gamma


class Cars:
    def __init__(self, start, end, score_mat):
        self.start = start
        self.end = end
        self.score_mat = score_mat
        self.policy = [[-1 for _ in range(grid_size)] for _ in range(grid_size)]

    @staticmethod
    def next_state(c, a):
        x_x = c[0]
        y_y = c[1]
        if a == 0:
            if x_x -1 <0:
                return c
            else:
                return [x_x-1, y_y]  
        if a == 1:
            if y_y +1 > grid_size - 1:
                return c
            else:
                return [x_x, y_y+1]
        if a == 2:
            if y_y - 1 <0:
                return c
            else: 
                return [x_x, y_y-1]
        if a == 3:
            if x_x + 1 > grid_size -1:
                return c
            else:
                return [x_x+1, y_y]
                
    @staticmethod
    def turn_left(direction):
        if direction == 0:
            return 2
        if direction == 1:
            return 0
        if direction == 2:
            return 3
        if direction == 3:
            return 1

    @staticmethod
    def turn_right(direction):
        if direction == 0:
            return 1
        if direction == 1:
            return 3
        if direction == 2:
            return 0
        if direction == 3:
            return 2

    def best_state(self, r, co, u_mat, flag):
        n_c = self.next_state([r, co], 0)
        e_c = self.next_state([r, co], 1)
        w_c = self.next_state([r, co], 2)
        s_c = self.next_state([r, co], 3)
        n_m = cr_p * u_mat[n_c[0]][n_c[1]] + diff_p * (
                u_mat[e_c[0]][e_c[1]] + u_mat[s_c[0]][s_c[1]] + u_mat[w_c[0]][w_c[1]])
        e_m = cr_p * u_mat[e_c[0]][e_c[1]] + diff_p * (
                u_mat[n_c[0]][n_c[1]] + u_mat[s_c[0]][s_c[1]] + u_mat[w_c[0]][w_c[1]])
        w_m = cr_p * u_mat[w_c[0]][w_c[1]] + diff_p * (
                u_mat[n_c[0]][n_c[1]] + u_mat[e_c[0]][e_c[1]] + u_mat[s_c[0]][s_c[1]])
        s_m = cr_p * u_mat[s_c[0]][s_c[1]] + diff_p * (
                u_mat[n_c[0]][n_c[1]] + u_mat[e_c[0]][e_c[1]] + u_mat[w_c[0]][w_c[1]])
        max_prob = max(n_m, e_m, w_m, s_m)
        if flag == 1:
            return max_prob, [n_m, e_m, w_m, s_m]
        return gamma * max_prob


    def val_iteration(self):
        u_prime = [x[:] for x in self.score_mat]
        u = [x[:] for x in self.score_mat]
        while True:
            d = 0
            for row in range(grid_size):
                for column in range(grid_size):
                    if row == self.end[0] and column == self.end[1]:
                        continue
                    u_prime[row][column] = self.score_mat[row][column] + self.best_state(row, column, u, 0)
                    if abs(u_prime[row][column] - u[row][column]) > d:
                        d = abs(u_prime[row][column] - u[row][column])
            if d < error_rate or time.time() - car_time_start > time_per_car:
                return u
            u = [x[:] for x in u_prime]

    def policy_extraction(self, optimal_val):
        u = [x[:] for x in optimal_val]
        for row in range(grid_size):
            for column in range(grid_size):
                if row == self.end[0] and column == self.end[1]:
                    continue
                max_prob, lst = self.best_state(row, column, u, 1)
                if max_prob == lst[0]:
                    self.policy[row][column] = 0
                elif max_prob == lst[3]:
                    self.policy[row][column] = 3
                elif max_prob == lst[1]:
                    self.policy[row][column] = 1
                else:
                    self.policy[row][column] = 2

        return self.policy


if __name__ == '__main__':
    input_list = [input_line.rstrip('\n\r') for input_line in open('input.txt')]
    grid_size = int(input_list[0])
    no_of_cars = int(input_list[1])
    time_per_car = 165/no_of_cars
    no_of_obstacles = int(input_list[2])
    total_obstacles = []
    cars_start = []
    cars_end = []

    for index in range(3, 3 + no_of_obstacles):
        x_coordinate, y_coordinate = input_list[index].split(',')
        x_c = int(y_coordinate)
        y_c = int(x_coordinate)
        total_obstacles.append([x_c, y_c])

    for index in range(3 + no_of_obstacles, 3 + no_of_obstacles + no_of_cars):
        x_coordinate, y_coordinate = input_list[index].split(',')
        cars_start.append([int(y_coordinate), int(x_coordinate)])

    for index in range(3 + no_of_obstacles + no_of_cars, 3 + no_of_obstacles + 2 * no_of_cars):
        x_coordinate, y_coordinate = input_list[index].split(',')
        x_co = int(y_coordinate)
        y_co = int(x_coordinate)
        cars_end.append([x_co, y_co])

    score_matrix = [[-1.0 for _ in range(grid_size)] for _ in range(grid_size)]

    for index in range(len(total_obstacles)):
        score_matrix[total_obstacles[index][0]][total_obstacles[index][1]] = -101.0  # Obstacle
       
    f_ptr = open('output.txt', 'w')
    
    lst = []
    
    for seed_counter in range(10):
        np.random.seed(seed_counter)
        swerve = np.random.random_sample(1000000)
        lst.append(swerve)
    
    for index in range(no_of_cars):
        
        car_time_start = time.time()

        obj = Cars(cars_start[index], cars_end[index], score_matrix)

        list_of_scores = []
        end_x = cars_end[index][0]
        end_y = cars_end[index][1]
        obj.score_mat[end_x][end_y] = 99.0

        optimal_values = obj.val_iteration()
        optimal_policy = obj.policy_extraction(optimal_values)
        
        for seed_counter in range(10):
            current = obj.start
            counter = 0
            swerve_index = 0
            swerve = lst[seed_counter]
            while current != cars_end[index]:
                current_move = optimal_policy[current[0]][current[1]]
                if swerve[swerve_index] > 0.7:
                    if swerve[swerve_index] > 0.8:
                        if swerve[swerve_index] > 0.9:
                            current_move = obj.turn_right(obj.turn_right(current_move))
                        else:
                            current_move = obj.turn_right(current_move)
                    else:
                        current_move = obj.turn_left(current_move)
                swerve_index += 1
                current = obj.next_state(current, current_move)
                counter += obj.score_mat[current[0]][current[1]]
            list_of_scores.append(counter)
        obj.score_mat[end_x][end_y] = -1.0
        f_ptr.write(str(int(sum(list_of_scores)/10))+'\n')
    f_ptr.close()
