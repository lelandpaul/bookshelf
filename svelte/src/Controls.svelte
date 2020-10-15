<style type="text/scss">
  #controls {
    padding-top: 3rem;
  }
</style>


<script>
  import { filter } from './stores.js';

  let shelve_by = [
    { id: 1, text: 'Year', categorize_by: 'year', source: 'reading'},
    { id: 2, text: 'Rating', categorize_by: 'rating', source: 'reading'}
  ]

  let sorts = [
    {id: 1, text: 'Date', sort_by: 'date'},
    {id: 2, text: 'Title', sort_by: 'book_title'}

  ]

  let selected_shelve = shelve_by[0];
  let selected_sort = sorts[0];

  export let categorize_by;
  export let source;
  export let sort_by;

  $: categorize_by = selected_shelve.categorize_by;
  $: source = selected_shelve.source;
  $: sort_by = selected_sort.sort_by;

</script>



<div id="controls" class="col-2">


    <form on:submit|preventDefault={()=>null}>

      <div class="form-group">
        <label for="filter-box">Filter:</label>
        <input id="filter-box" class="form-control" type="" bind:value={$filter}>
      </div>


      <div class="form-group">
        <label for="scheme-select">Shelve By:</label>
        <select bind:value={selected_shelve} 
                id="scheme-select"
                class="custom-select">
          {#each shelve_by as scheme}
            <option value={scheme}>
              {scheme.text}
            </option>
          {/each}
        </select>
      </div>
      <div class="form-group">
        <label for="sort-select">Sort By:</label>
        <select id="sort-select"
                class="custom-select"
                bind:value={selected_sort}>
              {#each sorts as sort}
                <option value={sort}>
                  {sort.text}
                </option>
              {/each}
        </select>
      </div>
    </form>

</div>
