const filterBySubstr = (arr, str, prefix) => (arr || []).map(
  n => (
    { 
      name: n.name, 
      id: n.id, 
      number: n.number,
      deleted: n.deleted,
      nodes: n.development_directions || n.skills || n.results || n.exercises,
      children: filterBySubstr(
        n.development_directions || n.skills || n.results || n.exercises,
        (prefix+n.number+'. '+n.name.toLowerCase()).includes(str) ? '' : str,
        prefix+n.number+'.'
      )
    })
).filter(
  n => (prefix+n.number+'. '+n.name.toLowerCase()).includes(str) || n.children.length
);

const filterByExercises = (arr, exercises, level=1) => (arr || []).map(
  n => (
    { 
      name: n.name, 
      id: n.id, 
      number: n.number,
      deleted: n.deleted,
      children: filterByExercises(
        n.development_directions || n.skills || n.results || n.exercises,
        exercises, level+1
      )
    })
).filter(
  n => {
    if (level === 5) {
      return exercises.includes(n.id);
    } else {
      return n.children.length;
    }
  }
);

const returnWithFormat = (arr) => (arr || []).map(
  n => (
    { 
      name: n.name, 
      id: n.id, 
      number: n.number,
      deleted: n.deleted,
      children: returnWithFormat(
        n.development_directions || n.skills || n.results || n.exercises,
      )
    })
);

export { filterBySubstr, filterByExercises };