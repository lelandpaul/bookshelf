<style type='text/scss'>
    @import './styles/vars.scss';
    .clickable {
        cursor: pointer;
    }

    .book {
        width: 15rem;
        height: 18rem;

        .title {
            white-space: pre-wrap;
        }

        ul.list-group {
            bottom:0;
            height: max-content;
        }

        .fa-book {
            font-size: 5rem;
            animation: pulse-black 2s infinite;
            border-radius: 10px;
        }

        .loading {
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .reading .fas {
          padding-top: 3px;
        }
    }

    @keyframes pulse-black {
    0% {
        transition-timing-function: ease;
        opacity: 50%;
    }
    
    50% {
        transition-timing-function: ease;
        opacity: 100%;
    }
    
    100% {
        transition-timing-function: ease;
        opacity: 50%;
    }
}

</style>



<script>
  import moment from 'moment';
  import { library, filter, detail } from './stores.js';
  export let book_id;

  $: book = $library[book_id-1];

</script>


{#await book}
<div class="book m-3 d-inline-block">
    <div class="loading">
        <i class="fas fa-book"></i>
    </div>
</div>
{:then book}
  <div class="book card m-3 align-bottom"
       class:d-none="{!book.full_text.includes($filter.toLowerCase())}"
       class:d-inline-block="{book.full_text.includes($filter.toLowerCase())}"
    >
    <div class="card-body"
      >
        <h5 class="card-title title clickable"
            data-toggle="modal" data-target="#detail-viewer" on:click={()=>$detail=book_id-1}
        >{book.title}</h5>
        {#each book.authors as author}
          <h6 class="card-subtitle mb-2 text-muted clickable"
              on:click={()=>$filter===author.surname ? $filter='' : $filter=author.surname}>
            {author.other_names} {author.surname}
        </h6>
        {/each}
    {#if book.series}
    <div class="series text-muted justify-content-between mt-2 mb-1">
            <span class="mr-auto">Series:</span>
            <span class="float-right clickable"
                  on:click={()=>$filter===book.series ? $filter='' : $filter=book.series}>
                {book.series}
            </span>
    </div>
    {/if}
    <div class="genres row mt-3">
        {#each book.genres as genre}
        <div class="col-auto my-1">
          <span class="badge badge-secondary clickable"
            on:click={()=>$filter===genre ? $filter='' : $filter=genre}
          >{genre}</span>
        </div>
        {/each}
    </div>
    </div>
    <ul class="list-group list-group-flush position-absolute w-100">
        {#each book.readings as reading}
        <li class="reading list-group-item py-1">
             <span class="reading-date">
                 {reading.year}: {moment(reading.date).format('MMMM Do')}
                 {#if reading.rating === 1}
                 <i class="fas fa-ban fa-fw align-text-bottom float-right"></i>
                 {:else if reading.rating === 3}
                 <i class="fas fa-star fa-fw align-text-bottom float-right"></i>
                 {/if}
                 {#if reading.reread}
                 <i class="fas fa-redo-alt fa-fw align-text-bottom float-right"></i>
                 {/if}
                 {#if reading.manner === 'audio'}
                 <i class="fas fa-headphones fa-fw align-text-bottom float-right"></i>
                 {/if}
                 {#if reading.manner === 'aloud'}
                 <i class="fas fa-user-friends fa-fw align-text-bottom float-right"></i>
                 {/if}
             </span>
         </li>
     {/each}
     </ul>
</div>
{/await}
