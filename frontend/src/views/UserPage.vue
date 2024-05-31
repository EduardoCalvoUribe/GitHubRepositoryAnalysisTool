<template>
  <header>
    <RouterLink to="/repoinfo/${id}">Repository Infomation</RouterLink>
    <RouterLink style="margin-left: 2%" to="/prpage">Pull Requests</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commitpage">Commits</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commentpage">Comments</RouterLink>
  </header>

  <RouterView />
  <header>
    <div style="font-size: 180%;  margin-top: 30px;">
      User page
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
