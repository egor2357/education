export default {
  methods: {
    formatSpecialist(specialist) {
      return specialist.patronymic
        ? `${specialist.surname}
              ${specialist.name[0]}.${specialist.patronymic[0]}.`
        : `${specialist.surname} ${specialist.name[0]}`;
    },
    formatSpecialistFull(specialist) {
      return specialist.patronymic
        ? `${specialist.surname} ${specialist.name} ${specialist.patronymic}`
        : `${specialist.surname} ${specialist.name}`;
    },
    isOnlyPositiveDigit(value) {
      return /^\d+$/.test(value);
    }
  },
};
