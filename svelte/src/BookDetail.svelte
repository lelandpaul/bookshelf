<style type="text/scss">
  $modal-min-width: 40rem;

  .modal-dialog {
    top: 5rem;
    /* max-width: unset; */
    width: 80%;
    /* min-width: $modal-min-width; */
    margin: auto;
  }

  .modal-content {
    width: max-content;
  }

  .reading .fas {
    opacity: 30%;
  }

  .fas.included {
    opacity: 100%;
  }

  :global(.nav-link.active) {
    font-weight: bold;
  }

</style>

<script>
  import { detail, library } from './stores.js';
  import moment from 'moment';


  $: book = $library[$detail];
  $: $library = $library;

  /* Fill series */
  async function getSeries(title){
    const promise = await fetch('./series?' +
                                'title=' + title);
      const text = await promise.json();
      if (promise.ok) {
          console.log('inner:', text);
          return text;
      } else {
          throw new Error(text);
      }
  }

  $: series = getSeries(book.series);
  $: console.log(series);


</script>

<div id="detail-viewer" class="modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-body">

        <div class="card-deck">

            <div class="card">
              <h3 class="card-header">{book.title}</h3>
              <div class="card-body">
                <div class="row my-3">
                  <div class="col">
                    <b>Series:</b>
                    {#if book.series == null}
                      <span class="float-right text-muted">none</span>
                    {:else}
                      <span class="float-right">{book.series}</span>
                    {/if}
                  </div>
                </div>
                <div class="row my-3">
                  <div class="col">
                    <b>Genres:</b>
                    {#each book.genres as genre}
                      <span class="float-right badge badge-secondary mx-1">{genre}</span>
                    {/each}
                  </div>
                </div>
                <div class="row my-3">
                  <div class="col">
                    <p><b>Readings:</b></p>
                    <ul class="list-group pt-1">
                      {#each book.readings as reading}
                        <li class="reading list-group-item py-1">
                            <div class="reading-date row no-gutters">
                              <div class="col-12 col-xl-6">
                                {reading.year}: {moment(reading.date).format('MMMM Do')}
                              </div>
                              <div class="col-12 col-xl-6 text-xl-right align-top">
                                  <i class="fas fa-star fa-fw"
                                    class:included={reading.rating >= 1}></i>
                                  <i class="fas fa-star fa-fw"
                                    class:included={reading.rating >= 2}></i>
                                  <i class="fas fa-star fa-fw"
                                    class:included={reading.rating >= 3}></i>
                                  <i class="fas fa-redo-alt fa-fw"
                                      class:included={reading.reread}></i>
                                  <i class="fas fa-headphones fa-fw"
                                    class:included={reading.manner === 'audio'}></i>
                                  <i class="fas fa-user-friends fa-fw"
                                    class:included={reading.manner === 'aloud'}></i>
                              </div>
                            </div>
                        </li>
                      {/each}
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <ul class="nav nav-tabs nav-justified card-header-tabs">
                  <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#author">
                      Author{#if book.authors.length > 1}s{/if}
                    </a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" 
                      data-toggle="tab" 
                      href="#series"
                      class:disabled={book.series == null}>Series</a>
                  </li>
                </ul>
              </div>
                <div class="card-body">
                  <div id="detailTabContent" class="tab-content">
                    <div class="tab-pane show active" id="author">
                      <ul class="list-group">
                        {#each book.authors as author}
                          <li class="list-group-item">
                            <div class="row">
                              <div class="col">{author.other_names}</div>
                              <div class="col text-muted">{author.gender}</div>
                              <div class="w-100"></div>
                              <div class="col"><h5>{author.surname}</div>
                              <div class="col text-muted">
                                {#if !author.white}
                                  non-
                                {/if}white
                              </div>
                            </div>
                          </li>
                        {/each}
                      </ul>
                    </div>
                    <div class="tab-pane" id="series">
                      <h5>{book.series}</h5>
                      {#await series then series}
                        <ul class="list-group">
                          {#each series as book}
                            <li class="list-group-item">
                              <div class="row">
                                <div class="col-1">
                                  {#if book.order}
                                    {book.order}
                                  {/if}
                                </div>
                                <div class="col">{book.book}</div>
                              </div>
                            </li>
                          {/each}
                        </ul>
                      {/await}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
