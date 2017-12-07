from sys import stdin

class LispInterpreter():
    def __init__(self):
        #Vars for brainf_ck
        self.counter_cells = 0
        self.cells = [0]

        #Define the available functions
        self.ARG_FUNCTION = {
            'add': self.add,  # > in brainfuck x times
            'sub': self.sub,     # < in brainfuck x times
            'do': self.do,
            'loop': self.loop,         # [] in brainfuck
            'do-before': self.do_before,
            'do-after': self.do_after,
        }

        self.N_ARG_FUNCTION = {
            'right': self.right,    # > in brainfuck
            'left': self.left,     # < in brainfuck
            'print': self._print,     # . in brainfuck
            'read': self.read,     # , in brainfuck
            'inc': self.inc,         # + in brainfuck
            'dec': self.dec,         # - in brainfuck
        }

    #Implement each function for lisp_f_ck
    def right(self):
        self.counter_cells += 1
        size_cells = len(self.cells)
        if self.counter_cells == size_cells:
            self.cells.append(0)

    def left(self):
        if self.counter_cells <= 0:
            self.counter_cells = 0
        else:
            self.counter_cells -= 1

    def inc(self):
        if self.cells[self.counter_cells] < 255:
            self.cells[self.counter_cells] = self.cells[self.counter_cells] + 1
        else:
            self.cells[self.counter_cells] = 0

    def dec(self):
        if self.cells[self.counter_cells] > 0:
            self.cells[self.counter_cells] = self.cells[self.counter_cells] - 1
        else:
            self.cells[self.counter_cells] = 255

    def sub(self, number):
        increment = number[0]
        while increment != 0:
            self.dec()
            increment = increment - 1

    def loop(self, code):
      while(self.cells[self.counter_cells]):
            self.do(code)

    def add(self, number):
        increment = number[0]
        while increment != 0:
            self.inc()
            increment = increment - 1

    def _print(self):
        content = chr(self.cells[self.counter_cells])
        print(content)

    def read(self):
        self.cells[self.counter_cells] = ord(stdin.read(1))
        ord(stdin.read(1))

    def do(self, code):
        for operation in code:
            if isinstance(operation, str):
                if operation in self.N_ARG_FUNCTION:
                    func = self.N_ARG_FUNCTION[operation]
                    func()
                else:
                    func = self.ARG_FUNCTION[operation]
                    func()
            else:
                self.run(operation)

    def do_before(self,code):
        before_command, command_list = code
        new_code = ['do']
        for command in command_list:
            new_code.extend([before_command, command])
        self.run(new_code)

    def do_after(self,code):
        after_command, command_list = code
        new_code = ['do']
        for command in command_list:
            new_code.extend([command, after_command])
        self.run(new_code)

    #Get the tree and run it
    def run(self, tree):
        head, *tail = tree

        if head in self.N_ARG_FUNCTION:
            self.N_ARG_FUNCTION[head]()
            return
        elif head in self.ARG_FUNCTION:
            func = self.ARG_FUNCTION[head]
            return func(tail)
        elif isinstance(head, int):
            return tail[0]
        else:
            raise ValueError('operador invalido: %s' % head)
