def fill_template(mpi_title, mpi_desc, mpi_keywords, mpi_content):

    return f'''<?php
    include("inc/vetKey.php");
    $h1 = "{mpi_title}";
    $title = $h1;
    $desc = "{mpi_desc}";
    $key = "{mpi_keywords}";
    $legendaImagem = "Foto ilustrativa de {mpi_title}";
    $pagInterna = "Informações";
    $urlPagInterna = "informacoes";
    include("inc/head.php");
    include("inc/fancy.php");
    ?>
    <style>
    <? include("css/style-icm.css"); ?>
    </style>
    <script>
    <? include("js/organictabs.jquery.js"); ?>
    </script>
    </head>
    <body class="mpi-rules">
    <? include("inc/topo-mpi.php"); ?>
    <main>
        <div class="content" itemscope itemtype="https://schema.org/Product">
            <div class="wrapper">
                <section>
                    <?=$caminho2?>
                    <h1><?=$h1?></h1>
                    
                    <article class="full">
                        <p class="content-call">Se você procura por <?=$h1?>, você encontra no website da <?=$nomeSite?>, cote produtos com nossos profissionais e conheça a melhor referência em qualidade do mercado.</p>
                        <div class="mpi-content" style="display: none;">
                            {mpi_content}
                        </div>
                        <a class="expand-content">
                            <span>Leia mais</span>
                        </a>
                    </article>
                    <article>
                        <?include("inc/gallery.php"); ?>
                    </article>
                    <?include("inc/mpi-post-content.php");?>
                </section>
                </div><!-- .wrapper -->
            </div>
        </main>
        <?include("inc/footer.php"); ?>
    </body>
    </html>'''