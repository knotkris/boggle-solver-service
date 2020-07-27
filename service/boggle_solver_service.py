DEFAULT_WORD_LENGTH = 3
en_dict_file_name = 'resources/words_alpha.txt'
# checks to see if the index is not out of range
def getValue(board, x, y, size):
    if (x < 0 or y < 0):
        return None
    if (x >= size or y >= size):
        return None
            
    return ((x * size) + y)


# maps board list to graph of all adjacent values
def create_board_graph(lst, size):
    graph = {}
    board = []
    for i in range(size): #convert list to 2-D list for processing the adjacent values easier
        board.append(lst[i*size:(i+1)*size])

    ind = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            children = [value for value in [getValue(board, row-1, col-1, size), getValue(board, row-1, col, size), getValue(board, row-1, col+1, size),
                        getValue(board, row, col-1, size), getValue(board, row, col+1, size),
                        getValue(board, row+1, col-1, size),getValue(board, row+1, col, size),getValue(board, row+1, col+1, size)] if value != None]

            graph[ind] = children
            ind += 1

    return graph

#bfs of adjancent values
def find_all_words(graph, lst, size, dictionary):
    #interate through dict keys
    word_cnt = 0
    for key in graph:
        curr_word = ''
        prev_char = ''
        visited = set()
        words = set() # to hold all validated words
        valid_words = []
        prefixes = set() # to prevent searching again for that specified path
        queue = [] # for each iteration clear queue
        queue.append((key, '')) # add current key to queue

        #while queue is not empty, pop key and iterate thourgh children adding them through the queue
        #maintain the prefix of the time of the child being added to the queue
        while(len(queue) > 0):
            key, prefix = queue.pop(0)
            
            if ((key, prefix) not in visited):
                curr_word = prefix + lst[key]
                if (len(curr_word) >= DEFAULT_WORD_LENGTH and curr_word not in prefixes):
                    if (curr_word not in words):
                        words.add(curr_word)
                        
                        if (curr_word in dictionary):
                                valid_words.append(curr_word)

                    prefixes.add(curr_word)
                
                children = graph.get(key)

                #only add the child if none of the letters exist in the current word
                queue.extend([(child, curr_word) for child in children
                              if lst[child] not in curr_word])
                
                visited.add((key, prefix))
    return valid_words

def find_words(board, size, word_dict):
        graph = create_board_graph(board, size)
        words = find_all_words(graph, board, size, word_dict)
        return words

def load_words():
    with open(en_dict_file_name) as word_file:
        valid_words = set(word_file.read().split())
        print('loaded file: ' + en_dict_file_name)
    
    return valid_words