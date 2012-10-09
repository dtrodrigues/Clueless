from twisted.application import internet, service
from clueserver import GameServerProtocol, GameFactory, GameService

port = 20000
interface = '0.0.0.0'

top_service = service.MultiService()

game_service = GameService()
game_service.setServiceParent(top_service)

factory = GameFactory(game_service)
tcp_service = internet.TCPServer(port, factory, interface=interface)
tcp_service.setServiceParent(top_service)

application = service.Application("twisted-game-server")

top_service.setServiceParent(application)
