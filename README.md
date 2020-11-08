# OCF Pulumi Configuration

This is where our Kubernetes cluster configuration goes.

## Folder Structure

- core: Things that are integral to cluster operation (CNI, Traefik, Rook, etc.)
- infra: Databases, update scripts (Postgres, MySQL, Adelie, etc.)
- apps: End-user services, anything serving HTTP (Grafana, Jenkins, Wordpress, etc.)

## Development

1. run [fydai's cluster setup script](https://gist.github.com/fydai/e8db5688e8327ebedeeb240caa494621) on your staff VM to get your very own personal Kubernetes
2. make changes to this configuration
3. `pulumi up`
4. IF !works GOTO 2
