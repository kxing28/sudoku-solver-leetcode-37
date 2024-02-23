class Solution:

    def is_x_in_row(self, row_num, x, board):
        row = self.get_row(row_num, board)
        row_nums = [int(n) for n in row if n.isnumeric()]
        # print(f"Num {x} Row {row_num} {row}")
        return x in row_nums
    
    def is_x_in_col(self, col_num, x, board):
        col = self.get_col(col_num, board)
        col_nums = [int(n) for n in col if n.isnumeric()]
        # print(f"Num {x} Col {col_num} {col}")
        return x in col_nums

    def is_x_in_box(self, box_num_x, box_num_y, x, board):
        box = self.get_box(box_num_x, box_num_y, board)
        box_nums = [int(n) for n in box if n.isnumeric()]
        # print(f"Num {x} Box {box_num_x} {box_num_y} {box}")
        return x in box_nums

    def get_row(self, row_num, board):
        row = board[row_num]
        return row
    
    def get_col(self, col_num, board):
        col = []
        for i in range(len(board)):
            col.append(board[i][col_num])
        return col
    
    def get_box(self, box_num_x, box_num_y, board):
        box = []
        for i in range(box_num_y*3, box_num_y*3+3):
            for j in range(box_num_x*3,box_num_x*3+3):
                box.append(board[i][j])
        return box

        
    def boardDeepCopy(self, board):
        copy = [[-1]*9 for i in range(9)]
        for i in range(len(board)):
            for j in range(len(board[0])):
                copy[i][j] = board[i][j]
        return copy

    def boardDeepCopyTo(self, origin, target):
        for i in range(len(origin)):
            for j in range(len(origin[0])):
                target[i][j] = origin[i][j]

    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # how do I know I can fill this cell in with this number x?
        # x is not in the same row, col, or box
        # AND this is the only cell that satisfies all those criteria against all other cells in the category row,col or box
        # i.e. x can only be in (1,2) if:
        #   x not in row 1
        #   x not in col 2
        #   x not in box 1
        #   AND 1 of the following:
        #   x cannot go in any other cells in row 1
        #       i.e. is x present in any col or box for this cell?
        #   OR
        #   x cannot got in any other cells in col 2
        #       i.e. is x present in any row or box for this cell?
        #   OR
        #   x cannot go in any other cells in box 1
        #       i.e. is x present in any row or col for this cell?

        # strategy:
        # make functions for is_x_in_row(row,x), is_x_in_col,is_x_in_box
        # for-loop through every cell
            # for-loop through every number
                # for numbers that aren't immediate no's to the first 3 conditions, turn to the next 3 conditions
                    # if none of the extra conditions are true, move on to the next number.

        # bifurcation -- there are only 2 possibilities, you can't go onwards without a guess.
        # recognize that there are only 2 possibilities
            # pick one, and mark down that we guessed here
            # move forward, if we get somewhere impossible -> recognize impossible board
                # or alternatively, recognize a situation where there are not 2 possibilities?
            # quantum - make a copy of the baord and perform both moves. See where it leads us.
            # if we get to a state where a cell has NO candidates. i.e. all nubmers can never go there,
            # then we have an error. We pop out to the most recent bifurcation, the board is deleted.
        # require: criteria on when to choose a bifurcation
        # require: recognize if no cells possible

        # we change things up a bit: for each cell, get_cell_candidates(). If len(arr) = 1 then we're good
        # if len(arr) = 0 then error, return
        # if len(arr) = 2 AND board hasn't changed since last time, then just pick one.

        flat_board = []
        old_flat_board = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                flat_board.append(board[y][x])

        candidates = [ [set([-1])]*9 for i in range(9)]
        
        while "." in flat_board and flat_board != old_flat_board:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    curr = board[i][j]
                    if curr != ".":
                        candidates[i][j] = set([-1])
                        continue
                    else:
                        # do algorithm
                        # populate cells
                        curr_set = set()
                        for n in range(1,10):
                            if self.is_x_in_row(i,n,board) or \
                               self.is_x_in_col(j,n,board) or \
                               self.is_x_in_box(j // 3, i // 3, n,board):
                                continue
                            else:
                                curr_set.add(n)
                        if len(curr_set) == 0:
                            # print("oops")
                            return (False, board)
                        candidates[i][j] = curr_set
            # now investigate the candidates
            # print(candidates)
            placed_flag = False
            for i in range(len(board)):
                for j in range(len(board[0])):
                    cand = candidates[i][j]
                    # if i == 3 and j == 3:
                        # print(f"{i} {j} {cand}")
                    if -1 in cand:
                        # placeholder set.
                        continue
                    full_cand_row = self.get_row(i, candidates)
                    full_cand_col = self.get_col(j, candidates)
                    full_cand_box = self.get_box(j//3,i//3,candidates)
                    # remove the current cell from each section
                    cand_row = full_cand_row[:j] + full_cand_row[j+1:]
                    cand_col = full_cand_col[:i] + full_cand_col[i+1:]
                    box_idx = 3*(j//3)+i//3
                    cand_box = full_cand_box[:box_idx] + full_cand_box[box_idx+1:]
                    # if i ==3 and j == 3:
                    #     print(cand_row)
                    #     print(cand_col)
                    #     print(cand_box)
                    for n in cand:
                        # look at entire row/col/box to see if n is in there
                        row_flag = True
                        col_flag = True
                        box_flag = True
                        for s in cand_row:
                            if n in s:
                                row_flag = False
                                break
                        for s in cand_col:
                            if n in s:
                                col_flag = False
                                break
                        for s in cand_box:
                            if n in s:
                                box_flag = False
                                break
                        if row_flag or col_flag or box_flag or len(cand) == 1:
                            board[i][j] = str(n)
                            candidates[i][j] = set([-1])
                            placed_flag = True
                            break
                    if placed_flag:
                        break
                if placed_flag:
                    break
            old_flat_board = flat_board
            flat_board = []
            for y in range(len(board)):
                for x in range(len(board[0])):
                    flat_board.append(board[y][x])
        # print(candidates)
        # recursion time. We've found everything we can without guessing.
        # we take a set of length 2 and perform a guess by filling in the board at that spot. Then we pass it back into solver.
        # if solver finds a solution, then it returns (True, board) so we assign board to its output.
        # if solver doesn't find a solution it prints "oops" and returns (False, board) so we know this isn't a good guess.
        # Then we'll need a dict telling us what guesses have been made already. It'll be the size of board and each elem will be a set with guessed values
        if "." in flat_board:
            copy = self.boardDeepCopy(board)
            for i in range(len(board)):
                for j in range(len(board[0])):
                    cand = candidates[i][j]
                    if -1 in cand or len(cand) > 2:
                        continue
                    for num in cand:
                        copy = self.boardDeepCopy(board)
                        copy[i][j] = str(num)
                        res, board_out = self.solveSudoku(copy)
                        # print(res)
                        if res:
                            self.boardDeepCopyTo(board_out, board)
                            return (True, board)
        return ("." not in flat_board, board)
