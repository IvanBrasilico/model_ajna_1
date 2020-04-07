Tensorflow serving testado em Ubuntu 16.04

## Gerando os modelos
Utilizar o código exemplo "Publicar modelos.ipynb" para gerar os arquivos do modelo.

Será gerado um diretório tfserving/<nomemodelo>/<versaomodelo>(Ex.: tfserving/peso/1). Nome e versão do modelo
devem ser informados no código, bem como criado um modelo Tensorflow2.0 e carregados os pesos.

Dentro deste diretório, o tensorflow save_model irá criar um arquivo .pb, e dois diretorios, assets e variables,
 contendo os pesos ativos no modelo.

Este diretório deve ser copiado para o Servidor.

## Exemplo de configuração de Servidor

Servidor CentOS 7
IP 10.68.100.90

1. Instalar docker se necessário

```shell script
$ sudo yum install docker
$ sudo service docker enable
$ sudo service docker start
```

2. Baixar arquivos do modelo

Os caminhos precisam ser modificados para o seu caso 

```shell script
$ cd /home/ivan
$ wget https://github.com/IvanBrasilico/model_ajna_1/raw/master/Publicacao_modelos/tfserving.tfzip
$ unzip tfserving.tfzip
```

3. Criar arquivo com o conteúdo abaixo em /home/ivan/tfserving 
```
model_config_list: {
  config: {
    name: "peso",
    base_path: "/models/peso",
    model_platform: "tensorflow" 
  },
  config: {
    name: "vazio",
    base_path: "/models/vazio",
    model_platform: "tensorflow" 
  }
}
```
 
 4. Iniciar tensorflow_model_server
 
##### TODO: Ver comando para container docker rodar na inicialização 

##### Importante: no CentOS, devido ao SELinux, o volume do docker dará um "Permission Error". Rode o comando abaixo para dar a permissão

```shell script
$ sudo chcon -Rt svirt_sandbox_file_t /home/ivan/tfserving
```
  
```shell script
$ sudo docker run -it -p 8501:8501 -v /home/ivan/tfserving:/models tensorflow/serving --model_config_file=models/model_config.config
```

Feito! Agora você pode fazer uma consulta em 8501, conforme exemplos de "Publicar modelos.ipynb"

Comando para testar se Servidor está no ar:

```shell script
$ curl http://localhost:8501/v1/model/vazio:predict -X POST
{'error': 'JSON Parse Error'}
```

 

