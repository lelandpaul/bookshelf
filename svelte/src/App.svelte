<script>
    import Shelf from './Shelf.svelte';
    import { library } from './stores.js';

    /* Fill library */

    $library = [...window.books];

    /* Fill shelves */
    async function getShelves(){
        const promise = await fetch('./shelves');
        const text = await promise.json();
        if (promise.ok) {
            return text;
        } else {
            throw new Error(text);
        }
    }

    let shelves = getShelves();

</script>

<main>
    {#await shelves}
        <p>...waiting</p>
    {:then shelves}
        {#each shelves as shelf}
            <Shelf label={shelf.label} books={shelf.books}/>
        {/each}
    {/await}
</main>

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
</style>
