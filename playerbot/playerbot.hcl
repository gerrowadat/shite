// Nomad job spec for playerbot
job "playerbot" {
  datacenters = ["home"]
  group "playerbot_servers" {
    task "playerbot_server" {
      driver = "docker" 
      config {
        image = "gerrowadat/playerbot:latest"
	volumes = [
		"/mnt/docker/playerbot:/config"
	]
        labels {
          group = "playerbot"
        }
      }
      resources {
        cpu = 512
        memory = 256
      }
    }
  }
}
