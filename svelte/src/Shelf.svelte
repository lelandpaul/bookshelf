<style type="text/scss">
    h4.category_label {
        top: 40%;
        translateY: -50%;
        margin-left: 2rem;
    } 
    #category_label{
      padding:0;
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

  /* This is a stupid hack:
  When all books are hidden by a filter, the shelf .col will have height 0.
  So we can then hide the label. (utterly bizarre that this works) */
  let h;

</script>


<div class="shelf row">
    <div id='category_label' class="col-1" class:d-none="{h === 0}">
        <h4 class="category_label position-absolute">
            {label}:
        </h4>
    </div>
    <div class="col"
         bind:clientHeight={h}>
        {#each books as book_id}
            <Book {book_id}/>
        {/each}
    </div>
</div>
