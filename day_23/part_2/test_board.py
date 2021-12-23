from main import initial_state, reachable_nodes


def test_hash_board_copy():
    board = initial_state("input_example.txt", part_2=False)

    new_board, _ = board.move_occupant(
        board.get_node(7),
        board.get_node(2),
        1,
    )
    assert hash(board) != hash(new_board)

    new_board, _ = new_board.move_occupant(
        new_board.get_node(2),
        new_board.get_node(7),
        1,
    )
    assert hash(board) == hash(new_board)


def test_move():
    board = initial_state("input_example.txt", part_2=False)

    new_board, _ = board.move_occupant(
        board.get_node(7),
        board.get_node(2),
        1,
    )

    assert new_board.get_node(7).occupants == "A"
    assert new_board.get_node(2).occupants == "B"
    assert board.get_node(7).occupants == "BA"
    assert board.get_node(2).occupants == ""


def test_reachable_nodes():
    board = initial_state("input_example.txt", part_2=False)
    nodes_with_distances = reachable_nodes(board, board.get_node(7))
    assert len(nodes_with_distances) == 7

    board, _ = board.move_occupant(board.get_node(7), board.get_node(1), 1)
    nodes_with_distances = reachable_nodes(board, board.get_node(7))
    assert len(nodes_with_distances) == 5


def test_move_generation():
    board = initial_state("input_example.txt", part_2=False)

    moves = board.generate_moves()
    assert len(moves) == 4 * 7


def test_completed():
    board = initial_state("input_completed.txt", part_2=False)

    assert board.completed


def test_one_from_each():
    board = initial_state("input_example.txt", part_2=False)

    board, _ = board.move_occupant(
        board.get_node(7),
        board.get_node(1),
        1,
    )
    board, _ = board.move_occupant(
        board.get_node(9),
        board.get_node(2),
        1,
    )
    board, _ = board.move_occupant(
        board.get_node(11),
        board.get_node(3),
        1,
    )
    board, _ = board.move_occupant(
        board.get_node(13),
        board.get_node(4),
        1,
    )

    moves = board.generate_moves()
    assert len(moves) == 2
