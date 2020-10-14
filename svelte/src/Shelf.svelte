<style type="text/scss">
    .category_label {
        top: 50%;
        translateY: -50%;
    } 
    .shelf .col {
        overflow-x:scroll;
        white-space: nowrap;
    }
</style>


<script>
    import Book from './Book.svelte';
    export let books;
    export let label;
</script>


<div class="shelf row">
    <div class="col-1">
        <h4 class="category_label position-absolute">
            {label}:
        </h4>
    </div>
    <div class="col">
        {#each books as book_id}
            <Book {book_id}/>
        {/each}
    </div>
</div>


