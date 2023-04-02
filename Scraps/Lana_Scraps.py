def get_most_similar(TextBlock: TeaxtBlock(Sentence("text sentence here"))):
    dale_chall_complexity(text)
    flesch_reading_ease(text)

    poss_similarity_text_block = read_csv("    ")
    min_diff = 100
    for textblock in poss_similarity_text_block:
        diff_dc = dc_score - textblock.dale_chall

        diff_fe = dc_score - textblock.dale_chall

        diff = diff_dc + diff_fe

        if diff <= min_diff:
            closest_text_block = textblock

    return closest_text_block.carec_m



def mean_dependency_distance_sentence(sentence: str) -> float:
    """Calculates the mean_dependency_distance given a sentence

    The Mean Dependency Distance (MDD) is:
    MDD(the sentence) = 1/(n-1) * summation of |D*Di| from i = 1 to n-1

    where DDi is the DD (dependency distance) of the ith syntactic link in the sentence.
    Note that the root of the sentence does not have a governor, and so will have a DD of 0.

    The dependency distance of adjacent words is 1, and dependency distance is defined
    as the (absolute) distance between the governor word and its dependent.

    Example:
        "The girl ate an apple" has dependencies:
        The: 1 (dependent of girl, dist 1)
        girl: 1 (dependent of ate, dist 1)
        ate: 0 (verb, has no governer, not dependent of anything)
        an: 1 (dependent of apple, dist 1)
        apple: 2 (dependent of ate, distance 2)
    """
    # Generally: this function calculates the distance between each word and its dependent in the sentence,
    # by traversing through the tree.
    # to calculate MDD, we begin with creating a dependency tree.
    tree = ct.nltk_spacy_tree(sentence, False)
    # tree.pretty_print()

    # Then, for each word in the tree, which we refer to as the ith word based on sentence position
    # we need to get, for every subtree, the distance between root and children if there is only one child.

    dependents = []
    return get_dependents(tree)
    # flatten(get_dependents(tree), dependents)
    # we can now take every pair to get their distances, by finding their position in the sentence.
    # Since dependency tree is formed left to right, going from i =0  to i = len(sentence) - 1
    # # will maintain the order in case of duplicates
    # distances = []
    # for i in range(0, len(sentence), 2):
    #     distances.append(abs(sentence.index(dependents[i], i - 1)
    #                          - sentence.index(dependents[i + 1], i - 1)))
    #
    # # lastly, summ all DDs and divide by num of words in sentence
    # return sum(distances) * 1 / (len(sentence)- 1)


def get_dependents(tree: ct.nltk.tree) -> list[list[ct.nltk.tree]] | None:
    """Get dependents in pairs

    Note that the NLTK built-in methods for ct.nltk.tree in this function add the following conditions:
    tree.subtrees() returns ALL the constituent trees, this includes the subtrees of its subtrees (and so on).
    It does not return ANY leaves, even those which are direct children of the tree's root.
    It also returns itself as one of the listed subtrees.

    tree.leaves() returns ALL the leaves across the full tree, ie all the descendants which are leaves

    tree.label() is analogous to the in-class tree._root, and returns the root value of the tree
    """
    # Then, for each word in the tree, which we refer to as the ith word based on sentence position,
    tree_root = tree.label()
    dependents = []

    # we need to get, for every subtree, the distance between root and children if there is a direct child leaf.
    # If the tree has leaves, cycle through the leaves in its subtrees, and collect all the leaves that are not also
    # leaves of its subtrees (these are the ones which are direct children of the root

    if len(tree.leaves()) >= 1:
        for leaf in tree.leaves():
            subtrees_sans_original = [subtree for subtree in tree.subtrees() if subtree.label() != tree_root]
            direct_leaf_condition = not any(leaf in subtree.leaves() for subtree in subtrees_sans_original)
            if direct_leaf_condition:
                dependents.append([tree_root, leaf])

    # Iterate through all subtrees (note that leaves are not included here), and if the subtree is not itself,
    # store the subtree's root and this tree's root in list of dependents
    # Recurse into the subtree to collect all the parent-child pairs inside
    for subtree in tree.subtrees():
        if subtree.label() != tree_root:
            # create a pair with root and every child, confirm that the subtree is a direct child of tree
            subtree_direct_child_of_tree_root = (subtree.height() == tree.height() - 1) \
                                                or [sub for sub in (subtree.subtrees())] == []
            if subtree_direct_child_of_tree_root:
                dependents.append([subtree.label(), tree_root])
            dependents.append(get_dependents(subtree))

    return dependents
