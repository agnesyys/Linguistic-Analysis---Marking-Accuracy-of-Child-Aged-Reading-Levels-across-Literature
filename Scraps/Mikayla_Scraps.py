"""Storage for Mikayla in case of Git Shenanigans"""
# import plotly.graph_objects as go
import nltk
# from courseProject.data_processing import TextBlock, Sentence
# from courseProject import complexity_measures as complex


# def display_reading_levels(book: TextBlock) -> None:
#     """Display a bar graph of the reading levels of a given novel."""
#     dc = complex.dale_chall_complexity(book)
#     fc = complex.flesch_complexity_score(book)
#     fig = go.Figure(
#         data=[go.Bar(y=[dc, fc, book.carec_m], x=['Dale-Chall Complexity', 'Flesch Complexity', 'CAREC'])],
#         layout_title_text="Reading Levels Computed by Different Algorithms"
#     )
#     fig.show()
#
#
# def display_reading_level_accuracy(textblock, dc: float, fc: float, sd: float) -> None:
#     """Display a bar graph of the reading level accuracy of a given sentence."""
#
#     fig = go.Figure(
#         data=[go.Bar(y=[dc, fc, sd, textblock.carec_m], x=['Dale-Chall Complexity', 'Flesch Complexity',
#                                                           'Syntatic Difficulty', 'CAREC_M'])],
#         layout_title_text="Reading Levels Accuracy Compared to CAREC M of '" + textblock.title + "'"
#     )
#     fig.show()


def get_dependents(tree: nltk.tree) -> list[list[nltk.tree]] | None:
    """Get dependents in pairs.

    Note: that the NLTK built-in methods for nltk.tree in this function add the following conditions:
    tree.subtrees() returns ALL the constituent trees, this includes the subtrees of its subtrees (and so on).
    It does not return ANY leaves, even those which are direct children of the tree's root.
    It also returns itself as one of the listed subtrees.

    tree.leaves() returns ALL the leaves across the full tree, i.e. all the descendants which are leaves

    tree.label() is analogous to the in-class tree.root, and returns the root value of the tree
    """
    # Then, for each word in the tree, which we refer to as the i-th word based on sentence position,
    tree_root = tree.label()
    dependents = []

    # for subtree in tree.subtrees():
    #     tree.

    # we need to get, for every subtree, the distance between root and children if there is a direct child leaf.
    # if len(tree.leaves()) >= 1:
    #     for leaf in tree.leaves():
    #         subtrees_sans_original = [subtree for subtree in tree.subtrees() if subtree.label() != tree_root]
    #         direct_leaf_condition = not any(leaf in subtree.leaves() for subtree in subtrees_sans_original)
    #         if direct_leaf_condition:
    #             dependents.append([tree_root, leaf])
    # print(dependents)
    # # Iterate through all subtrees (note that leaves are not included here), and if the subtree is not itself,
    # # store the subtree's root and this tree's root in list of dependents
    # # Recurse into the subtree to collect all the parent-child pairs inside
    # for subtree in tree.subtrees:
    #     if subtree.label() != tree_root:
    #         dependents.append([tree_root, subtree.label()])

    return dependents
