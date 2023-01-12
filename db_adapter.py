import btree


class db_adapter:
    def __init__(self) -> None:
        try:
            self.f = open("saved_params", "r+b")
        except OSError:
            self.f = open("saved_params", "w+b")

        self.db = btree.open(self.f)
        self._index = 1
        self.btree_index = None

    def save_waveform_params(self, param_packet):
        if self._index == 1:
            pass
        else:
            self._index + 1

        self.btree_index = b'{str(self._index)}'.__format__(self._index)
        self.db[self.btree_index] = b'{param_packet}'.__format__(
            param_packet=param_packet)
        # flush cache after each tx
        self.db.flush()

    def delete_params(self, params_index):
        b_params_index = b'{params_index}'.__format__(b_params_index)
        del self.db[b_params_index]
        print(self, params_index)

    def list_saved_params(self):
        for params in self.db.values():
            print(params)
