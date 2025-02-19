export default {
  methods: {
    formatSpecialist(specialist) {
      // return specialist.patronymic
      //   ? `${specialist.surname}
      //         ${specialist.name[0]}.${specialist.patronymic[0]}.`
      //   : `${specialist.surname} ${specialist.name[0]}`;
      let result = specialist.surname;
      if (specialist.name)
        result += ` ${specialist.name[0]}.`;
      if (specialist.patronymic)
        result += ` ${specialist.patronymic[0]}.`;
      return result;
    },
    formatSpecialistFull(specialist) {
      // return specialist.patronymic
      //   ? `${specialist.surname} ${specialist.name} ${specialist.patronymic}`
      //   : `${specialist.surname} ${specialist.name}`;
      let result = specialist.surname;
      if (specialist.name)
        result += ` ${specialist.name}`;
      if (specialist.patronymic)
        result += ` ${specialist.patronymic}`;
      return result;
    },
    isOnlyPositiveDigit(value) {
      return /^\d+$/.test(value);
    }
  },
};
