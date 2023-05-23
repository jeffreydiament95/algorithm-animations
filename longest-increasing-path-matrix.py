from manim import *

class LongIncPathMatrix(Scene):
    def construct(self):
        # Define the matrices
        matrix = [[9,9,4],[6,6,8],[2,1,1]]
        memo = [[0,0,0],[0,0,0],[0,0,0]]
        
        buff_size = 1.5
        matrix_mob = IntegerMatrix(matrix, h_buff=buff_size, v_buff=buff_size)
        memo_mob = IntegerMatrix(memo, h_buff=buff_size, v_buff=buff_size)

        # Define the labels
        label_1 = Text("MxN matrix").scale(0.5)
        label_2 = Text("Memoization Matrix").scale(0.5)

        # Group matrix with its label
        group_1 = VGroup(label_1, matrix_mob).arrange(DOWN)
        group_2 = VGroup(label_2, memo_mob).arrange(DOWN)

        # Position matrices side by side
        matrices = VGroup(group_1, group_2).arrange(buff=1)

        # Add matrices to scene
        self.play(Write(matrices))
    
        # Find the longest path and update the memoization matrix
        longest_path = self.find_longest_path(matrix, memo, matrix_mob, memo_mob)

        # # Show the result
        result = Text("Longest Path: " + str(longest_path)).scale(0.75)
        result.next_to(matrices, DOWN)
        self.play(Write(result))

    def draw_matrix(self, matrix):
        matrix_mob = []
        for i, row in enumerate(matrix):
            row_mob = []
            for j, value in enumerate(row):
                cell = Text(str(value)).scale(0.5)
                cell.move_to(RIGHT * j + UP * i)
                row_mob.append(cell)
                self.add(cell)
            matrix_mob.append(VGroup(*row_mob))
        return VGroup(*matrix_mob)

    def two_dim_to_one_dim(self, i, j, num_columns):
        return i * num_columns + j



    def find_longest_path(self, matrix, memo, matrix_mob, memo_mob):
        m, n = len(matrix), len(matrix[0])

        # Initialize direction matrix with None
        direction = [[None]*n for _ in range(m)]
        
        def dfs(i, j):
            index = self.two_dim_to_one_dim(i, j, n)
            
            # Create a box around the middle element of matrix_1
            box = (SurroundingRectangle(matrix_mob.get_entries()[index], color=RED))
            dashed_box = DashedVMobject(box)
            self.play(Create(dashed_box))
            
            if memo[i][j] != 0:
                return memo[i][j]

            max_path = 1
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for dy, dx in directions:
                y, x = i + dy, j + dx
                if 0 <= y < m and 0 <= x < n and matrix[y][x] > matrix[i][j]:
                    new_index = self.two_dim_to_one_dim(y, x, n)
                    # arrow_scale = 1.5 if dy != 0 else 1  # Increase size of vertical arrows
                    arrow_scale = 1
                    arrow_matrix = Arrow(matrix_mob.get_entries()[index].get_center(), matrix_mob.get_entries()[new_index].get_center(), buff=0.3).scale(arrow_scale)
                    arrow_memo = Arrow(memo_mob.get_entries()[index].get_center(), memo_mob.get_entries()[new_index].get_center(), buff=0.3).scale(arrow_scale)
                    self.play(Create(arrow_matrix), Create(arrow_memo))
                    max_path = max(max_path, dfs(y, x) + 1)
                    self.play(FadeOut(arrow_memo))
                    

            memo[i][j] = max_path
            memo_mob.get_entries()[index].set_value(max_path)
            self.play(FadeOut(dashed_box), Create(box))

            return max_path

        longest_path = 0
        for i in range(m):
            for j in range(n):
                dfs(i, j)
                
        self.draw_longest_path(matrix, memo, matrix_mob, memo_mob)
        longest_path = max([max(row) for row in memo])
        
        return longest_path
    
    def draw_longest_path(self, matrix, memo, matrix_mob, memo_mob):
        # Get the index of the maximum path length in the memo matrix
        max_value = max(max(row) for row in memo)
        for i, row in enumerate(memo):
            for j, value in enumerate(row):
                if value == max_value:
                    index = (i, j)
                    break
            else:
                continue
            break
        
        # trace the path back to the start and draw green arrows on the memo matrix along the way
        # while True: