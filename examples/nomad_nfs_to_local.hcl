// This is an example nomad jobspec for a job that wants to work from a local directory
// (my home setup uses an NFS server and some stuff (like sqlite3 in certain modes) doesn't
// play nice with nfs). It's an exampe of nomad's pre/post-flight and sidecar task syntax.

// Remember that raw_exec is disabled by default. See https://www.nomadproject.io/docs/drivers/raw_exec

job "examplejob" {
  datacenters = ["home"]
  group "examplejob-servers" {

    // pre-flight task to copy the job directory from NFS.
    task "copy-examplejob-dir-to-local" {
      lifecycle {
        hook = "prestart"
        sidecar = false
      }
      driver = "raw_exec"
      config {
        command = "/usr/bin/rsync"
        args = ["-carv", "--delete", "/mnt/docker/examplejob/", "/local/examplejob/"]
      }
    }


    // The sidecar job that re-syncs the job directory to NFS every hour.
    task "sync-examplejob-dir-to-remote" {
      lifecycle {
        hook = "poststart"
        sidecar = true
      }
      driver = "raw_exec"
      config {
        command = "/bin/sh"
        args = ["-c", "while true; do sleep 3600; /usr/bin/rsync -carv --delete /local/examplejob/ /mnt/docker/examplejob/; done"]
      }
    }

    // The post-flight job that re-syncs the job directory to NFS when the task is stopped cleanly.
    task "copy-examplejob-dir-to-remote" {
      lifecycle {
        hook = "poststop"
        sidecar = false
      }
      driver = "raw_exec"
      config {
        command = "/usr/bin/rsync"
        args = ["-carv", "--delete", "/local/examplejob/", "/mnt/docker/examplejob/"]
      }
    }

    // The job itself.
    task "examplejob" {
      driver = "docker" 
      config {
        image = "gerrowadat/examplejob"
        volumes = [
          "/local/examplejob:/config",
        ]
        labels {
          group = "examplejob-servers"
        }
        ports = ["examplejob-webui"]
      }
      resources {
        cpu = 2000
        memory = 1024
      }
      env {
        PUID = "1001"
        TZ = "Europe/Dublin"
      }
    }
    network {
      port "examplejob-webui" {
        static = "12345"
      }
    }

  }
}
