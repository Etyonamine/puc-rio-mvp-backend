from schemas.error import ErrorSchema

from schemas.marca import MarcaSchema,MarcaEditSchema, apresenta_marca,ListaMarcasSchema,\
                          apresenta_lista_marca,MarcaBuscaDelSchema, MarcaViewSchema

from schemas.modelo import ModeloSchema,ModeloEditSchema,ModeloBuscaDelSchema, ModeloViewSchema,ListaModelosSchema,\
                           apresenta_modelo,apresenta_lista_modelo,ModeloBuscaPorMarcaSchema

from schemas.veiculo import VeiculoSchema,VeiculoViewSchema,VeiculoEditSchema,VeiculoBuscaDelSchema,\
                            ListaVeiculosSchema,apresenta_lista_veiculo,apresenta_veiculo, VeiculoBuscaPorModelo