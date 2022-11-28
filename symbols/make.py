from symbols import Node, literal, binary


class MakeError(RuntimeError):
    pass


def polynomial(coef: list[float], variable: literal.Literal | None = None) -> Node:
    if len(coef) == 0:
        raise MakeError("cannot create a polynomial of order zero")

    if variable is None:
        variable = literal.Variable()

    root = binary.Mul(literal.Real(coef[0]), variable.copy())
    for index, c in enumerate(coef[1:]):
        if c == 0:
            continue

        root = binary.Add(
            root,
            binary.Mul(
                literal.Real(c),
                binary.Pow(
                    variable.copy(),
                    literal.Int(index+1)
                )
            )
        )

    return root
