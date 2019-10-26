class Music:
    def __init__(self, note):
        self.__notes = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
        self.__open_pos_chords = ['A','Am','C','D','Dm','E','Em','G']

        if note[-1] == 'b':
            p = self.__note_position_in_list(note[:-1])
            self.__note = self.__notes[p-1]
        else:
            self.__note = note
        '''if len(self.__note) > 2:
            return None
        elif len(self.__note) == 2 and self.__note[1] != '#' or self.__note[1] != 'b':
            return None
        
        self.__note = self.__note[0].upper() + self.__note[1:]'''
        self.__tone = 2
        self.__semi_tone = 1
        self.__major = ''
        self.__minor = 'm'
        self.__diminished = 'dim'
        self.__maj_scale_formula = [self.__tone,self.__tone,self.__semi_tone,self.__tone,self.__tone,self.__tone,self.__semi_tone]
        self.__chord_prog_in_maj_scale_formula = [self.__major,self.__minor,self.__minor,self.__major,self.__major,self.__minor,self.__diminished]
        self.__min_scale_formula = [self.__tone,self.__semi_tone,self.__tone,self.__tone,self.__semi_tone,self.__tone,self.__tone]
        self.__chord_prog_in_min_scale_formula = [self.__minor,self.__minor,self.__major,self.__major+'/'+self.__minor,self.__major+'/'+self.__minor,self.__major,self.__major]

    def __note_position_in_list(self, note):
        for i in range(len(self.__notes)):
            if self.__notes[i] == note:
                return i
    
    def valid_note(self, note):
        if note in self.__notes: # Make this list to represent as 'b' along with '#'; w.r.t input (#/b)
            return True
        return False

    def major_scale(self):
        position = self.__note_position_in_list(self.__note)

        notes_in_scale = [self.__notes[position]]
        
        for i in range(6):
            position = position + self.__maj_scale_formula[i]
            if position >= len(self.__notes):
                position = position % len(self.__notes)
            notes_in_scale.append(self.__notes[position])

        return notes_in_scale

    def __major_scale(self, note):
        position = self.__note_position_in_list(note)

        notes_in_scale = [self.__notes[position]]
        
        for i in range(6):
            position = position + self.__maj_scale_formula[i]
            if position >= len(self.__notes):
                position = position % len(self.__notes)
            notes_in_scale.append(self.__notes[position])

        return notes_in_scale

    def major_chord(self):
        scale = self.major_scale()
        return [scale[0], scale[2], scale[4]]

    def notes_in_major_scale(self):
        scale = self.major_scale()
        for i in range(len(scale)):
            scale[i] = scale[i] + self.__chord_prog_in_maj_scale_formula[i]
        return scale

    def __notes_in_major_scale(self, note):
        scale = self.__major_scale(note)
        for i in range(len(scale)):
            scale[i] = scale[i] + self.__chord_prog_in_maj_scale_formula[i]
        return scale

    def note_in_major_scales(self):
        notes_scales = []
        scales = []
        for i in range(len(self.__notes)):
            notes_scales.append(self.__major_scale(self.__notes[i]))
        
        for i in range(12):
            for j in range(7):
                if self.__note == notes_scales[i][j]:
                    scales.append(notes_scales[i][0])
        return scales

    def capo_pos_note_shift(self, capo_pos = 0):
        position = 0
        for i in range(len(self.__notes)):
            if self.__notes[i] == self.__note:
                position = i

        new_note = self.__notes[position - capo_pos]
        return new_note

    def capo_pos_scale_shift(self, capo_pos = 0):
        new_note = self.capo_pos_note_shift(capo_pos)
        new_scale = self.__notes_in_major_scale(new_note)
        return new_scale

    def minor_scale(self):
        position = self.__note_position_in_list(self.__note)

        notes_in_scale = [self.__notes[position]]
        
        for i in range(6):
            position = position + self.__min_scale_formula[i]
            if position >= len(self.__notes):
                position = position % len(self.__notes)
            notes_in_scale.append(self.__notes[position])

        return notes_in_scale

    def notes_in_minor_scale(self):
        scale = self.minor_scale()
        for i in range(len(scale)):
            if '/' in self.__chord_prog_in_min_scale_formula[i]:
                join_formula = '/' + scale[i]
                scale[i] = scale[i] + self.__chord_prog_in_min_scale_formula[i]
                parts = scale[i].split('/')
                scale[i] = join_formula.join(parts)+' '
            else:
                scale[i] = scale[i] + self.__chord_prog_in_min_scale_formula[i]
        return scale

    def open_pos_chords(self):
        pass
