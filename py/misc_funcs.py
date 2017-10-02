

def make_format(current, other):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        display_coord = current.transData.transform((x, y))
        inv = other.transData.inverted()
        # convert back to data coords with respect to ax
        ax_coord = inv.transform(display_coord)
        coords = [ax_coord, (x, y)]
        return ('Left: {:<40}    Right: {:<}'
                .format(*['({:.3f}, {:.3f})'.format(x, y) for x, y in coords]))
    return format_coord
