<style type="text/scss">

  @import './styles/vars.scss';

	main {
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: $color;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

  :global(.container-fluid){
    max-width: 95vw;
    margin-top: 3rem;

  }

</style>

<script>
  import Shelf from './Shelf.svelte';
  import Controls from './Controls.svelte';
  import { library } from './stores.js';

  /* Fill library */

  $library = [...window.books];

  /* Fill shelves */
  async function getShelves(cat,src,sort){
    console.log(typeof cat)
    if (typeof cat === 'undefined') {
      console.log('took the branch')
      return {label: '...', books: ''}
    }
    const promise = await fetch('./shelves?' +
                                'categorize_by=' + cat +
                                '&source=' + src +
                                '&sort_by=' + sort);
      const text = await promise.json();
      if (promise.ok) {
          return text;
      } else {
          throw new Error(text);
      }
  }

  let categorize_by;
  let source;
  let sort_by;

  $: shelves = getShelves(categorize_by, source, sort_by);

</script>

<main class="row">
  <Controls bind:categorize_by={categorize_by}
            bind:source={source}
            bind:sort_by={sort_by}/>
    <div class="col-10">
      {#await shelves}
          <p>...waiting</p>
      {:then shelves}
          {#each shelves as shelf}
              <Shelf label={shelf.label} books={shelf.books}/>
          {/each}
      {/await}
    </div>
</main>
