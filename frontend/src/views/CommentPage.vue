<template>
    <header>

    <RouterLink to="/repoinfo/1">Repository Infomation</RouterLink>
    <RouterLink to="/prpage">Pull Requests</RouterLink>
    <RouterLink to="/commitpage">Commits</RouterLink>
    <RouterLink to="/commentpage">Comments</RouterLink>

  </header>

  <RouterView />
    <header>
      <div style="font-size: 180%;">
        Comment Page
      </div>
    </header>
</template>

<style>
@media (min-width: 1024px) {
    .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
    }
}
</style>