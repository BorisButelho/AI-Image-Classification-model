from deity_rules import DEITY_RULES


def infer_deities(detected_labels):

    scores = {}
    matched_clues = {}

    for deity, attributes in DEITY_RULES.items():
        score = 0
        clues_used = []

        # Direct deity detection (strong signal)
        if deity in detected_labels:
            score += 3
            clues_used.append(deity)

        # Symbolic correlation
        for clue in attributes.keys():
            if clue in detected_labels:
                score += 1
                clues_used.append(clue)

        if score > 0:
            scores[deity] = score
            matched_clues[deity] = clues_used

    if not scores:
        return {}, {}

    return scores, matched_clues
