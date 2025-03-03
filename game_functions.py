

class Game:
    '''
    
    # Classe de inicialização do jogo.
    
    '''

    def __init__(self):
        pass



class Tabuleiro:
    def __init__(self):
        # Criação dos mini tabuleiros
        self.miniTabuleiro0 = miniTabuleiro()
        self.miniTabuleiro1 = miniTabuleiro()
        self.miniTabuleiro2 = miniTabuleiro()
        self.miniTabuleiro3 = miniTabuleiro()
        self.miniTabuleiro4 = miniTabuleiro()
        self.miniTabuleiro5 = miniTabuleiro()
        self.miniTabuleiro6 = miniTabuleiro()
        self.miniTabuleiro7 = miniTabuleiro()
        self.miniTabuleiro8 = miniTabuleiro()

        #self.alt_valor_celula(0, (0, 0), "X")
        #self.alt_valor_celula(0, (1, 1), "X")
        #self.alt_valor_celula(0, (2, 2), "X")

    def cria_miniTabuleiro(self):
        grid = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self.celulavazia)  # Usando "-" para representar células vazias
            grid.append(row)
        return grid

    def print_miniTabuleiroOnSelect(self, miniTabuleiroID):
        # Criação de um tabuleiro vazio para referência visual
        tabuleiro_vazio = [[" " for _ in range(3)] for _ in range(3)]

        # Determina a linha e coluna do mini tabuleiro selecionado
        linha = miniTabuleiroID // 3
        coluna = miniTabuleiroID % 3

        # Insere um marcador na posição do mini tabuleiro selecionado
        tabuleiro_vazio[linha][coluna] = "◯"

        # Imprime o tabuleiro com a indicação do mini tabuleiro selecionado
        print("╔═══╦═══╦═══╗")
        for i in range(3):
            print("║", " ║ ".join(tabuleiro_vazio[i]), "║")
            if i < 2:
                print("╠═══╬═══╬═══╣")
        print("╚═══╩═══╩═══╝")



    def print_Tabuleiro(self):
        print("   ┌───────┬───────┬───────┐  ||  ┌───────┬───────┬───────┐  ||  ┌───────┬───────┬───────┐")
        
        for linha in range(3):  # Percorre as 3 linhas de mini tabuleiros
            for i in range(3):  # Percorre as 3 linhas dentro de cada mini tabuleiro
                linha_atual = []  # Inicializa a linha sem rótulos
                
                for coluna in range(3):  # Percorre os 3 mini tabuleiros da linha
                    mini_tabuleiro = getattr(self, f"miniTabuleiro{linha * 3 + coluna}")  # Acessa o mini tabuleiro
                    mini_tabuleiro_grid = mini_tabuleiro.grid
                    linha_atual.append("   │   ".join(str(mini_tabuleiro_grid[i][j]) for j in range(3)))  # Junta a linha do mini tabuleiro
                
                print("   │  ", "   │      │   ".join(linha_atual), "  │")  # Monta a linha com separadores entre os mini tabuleiros
                
                if i < 2:
                    print("   ├───────┼───────┼───────┤  ||  ├───────┼───────┼───────┤  ||  ├───────┼───────┼───────┤")
            
            if linha < 2:
                print("   └───────┴───────┴───────┘  ||  └───────┴───────┴───────┘  ||  └───────┴───────┴───────┘")
                print("  =========================================================================================")
                print("   ┌───────┬───────┬───────┐  ||  ┌───────┬───────┬───────┐  ||  ┌───────┬───────┬───────┐")

        print("   └───────┴───────┴───────┘  ||  └───────┴───────┴───────┘  ||  └───────┴───────┴───────┘")

    def alt_valor_celula(self, mini_tabuleiroID, pos, valor):
        mini_tabuleiro = getattr(self, f"miniTabuleiro{mini_tabuleiroID}")
        mini_tabuleiro_grid = mini_tabuleiro.grid
        mini_tabuleiro_grid[pos[0]][pos[1]] = valor

    def get_valor_celula(self, mini_tabuleiroID, pos):
        mini_tabuleiro = getattr(self, f"miniTabuleiro{mini_tabuleiroID}")
        return mini_tabuleiro[pos[0]][pos[1]]
                    
class miniTabuleiro:
    def __init__(self):
        # Define interior do tabuleiro
        self.celulavazia = " "
    
        grid = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self.celulavazia)  # Usando "-" para representar células vazias
            grid.append(row)

        self.grid = grid     

    def print_miniTabuleiro(self, grid):
        print("    1   2   3 ")
        print("  ┌───┬───┬───┐")
        for i, row in enumerate(["1", "2", "3"]):
            print(row, "│", " │ ".join(str(grid[i][j]) for j in range(3)), "│")
            if i < 2:
                print("  ├───┼───┼───┤")
        print("  └───┴───┴───┘")

    def checar_vitoria_miniTabuleiro(self):
        # Verifica linhas e colunas
        for i in range(3):
            if self.grid[i][0] != self.celulavazia and self.grid[i][0] == self.grid[i][1] == self.grid[i][2]:
                return self.grid[i][0]  # Retorna o valor vencedor
            if self.grid[0][i] != self.celulavazia and self.grid[0][i] == self.grid[1][i] == self.grid[2][i]:
                return self.grid[0][i]

        # Verifica diagonais
        if self.grid[0][0] != self.celulavazia and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            return self.grid[0][0]
        if self.grid[0][2] != self.celulavazia and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            return self.grid[0][2]

        return None  # Retorna None se não houver vencedor

    


#grid = Tabuleiro.cria_miniTabuleiro()
#Tabuleiro.print_miniTabuleiro(grid)

tabuleiro = Tabuleiro()
tabuleiro.print_miniTabuleiroOnSelect(1)

tabuleiro.alt_valor_celula(1, (2, 2), "A")
tabuleiro.alt_valor_celula(8, (1,1), "E")
tabuleiro.alt_valor_celula(4, (2, 2), "A")
tabuleiro.alt_valor_celula(8, (0,0), "E")
tabuleiro.alt_valor_celula(0, (2, 2), "A")
tabuleiro.alt_valor_celula(8, (2,2), "E")
tabuleiro.print_Tabuleiro()
print(tabuleiro.miniTabuleiro8.checar_vitoria_miniTabuleiro())


