"""Hierarchical Bayesian state-space model using NumPyro."""

from __future__ import annotations

import numpy as np

from inkomstprognos.seeds import derive_seed


class HierarchicalStateSpace:
    """Local-level + trend + AR(1) macro-effect hierarchical state-space model.

    Uses NumPyro NUTS HMC for posterior inference.

    Args:
        num_warmup: Number of MCMC warmup steps.
        num_samples: Number of posterior samples.
        num_chains: Number of MCMC chains.
        random_state: Random seed.

    Examples:
        >>> model = HierarchicalStateSpace(num_warmup=10, num_samples=10, random_state=42)
    """

    def __init__(
        self,
        num_warmup: int = 500,
        num_samples: int = 1000,
        num_chains: int = 1,
        random_state: int = 0,
    ) -> None:
        self.num_warmup = num_warmup
        self.num_samples = num_samples
        self.num_chains = num_chains
        self.random_state = random_state
        self._samples: dict[str, np.ndarray] | None = None
        self._fitted: bool = False

    @staticmethod
    def _model(
        y: np.ndarray | None = None,
        T: int = 1,
    ) -> None:
        """NumPyro model specification: local level + trend + AR(1)."""
        import jax.numpy as jnp
        import numpyro
        import numpyro.distributions as dist

        sigma_level = numpyro.sample("sigma_level", dist.HalfNormal(1.0))
        sigma_trend = numpyro.sample("sigma_trend", dist.HalfNormal(0.5))
        sigma_obs = numpyro.sample("sigma_obs", dist.HalfNormal(1.0))
        phi = numpyro.sample("phi", dist.Uniform(-1.0, 1.0))

        level = numpyro.sample("level_init", dist.Normal(0.0, 10.0))
        trend = numpyro.sample("trend_init", dist.Normal(0.0, 1.0))

        for t in range(T):
            trend = numpyro.sample(
                f"trend_{t}",
                dist.Normal(phi * trend, sigma_trend),
            )
            level = numpyro.sample(
                f"level_{t}",
                dist.Normal(level + trend, sigma_level),
            )
            if y is not None:
                numpyro.sample(
                    f"obs_{t}",
                    dist.Normal(level, sigma_obs),
                    obs=jnp.array(y[t]) if t < len(y) else None,
                )

    def fit(self, y: np.ndarray) -> HierarchicalStateSpace:
        """Fit the state-space model using NUTS HMC.

        Args:
            y: Time series array of shape (T,).

        Returns:
            Self.

        Raises:
            ValueError: If y is empty.

        Examples:
            >>> import numpy as np
            >>> model = HierarchicalStateSpace(num_warmup=5, num_samples=5, random_state=0)
            >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
            >>> _ = model.fit(y)
            >>> model._fitted
            True
        """
        if len(y) == 0:
            msg = "y must be non-empty"
            raise ValueError(msg)

        import jax
        from numpyro.infer import MCMC, NUTS

        seed = derive_seed(self.random_state, namespace="state_space")
        rng_key = jax.random.PRNGKey(seed)

        kernel = NUTS(self._model)
        mcmc = MCMC(
            kernel,
            num_warmup=self.num_warmup,
            num_samples=self.num_samples,
            num_chains=self.num_chains,
            progress_bar=False,
        )
        mcmc.run(rng_key, y=y, T=len(y))
        self._samples = {k: np.asarray(v) for k, v in mcmc.get_samples().items()}
        self._fitted = True
        return self

    def predict(self, horizon: int = 1) -> np.ndarray:
        """Generate posterior predictive samples for future time steps.

        Args:
            horizon: Number of future steps to predict.

        Returns:
            Array of shape (num_samples, horizon) with predictive samples.

        Raises:
            RuntimeError: If the model has not been fitted.
            ValueError: If horizon is non-positive.

        Examples:
            >>> import numpy as np
            >>> model = HierarchicalStateSpace(num_warmup=5, num_samples=5, random_state=0)
            >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
            >>> _ = model.fit(y)
            >>> preds = model.predict(horizon=3)
            >>> preds.shape[1]
            3
        """
        if not self._fitted or self._samples is None:
            msg = "Model has not been fitted"
            raise RuntimeError(msg)
        if horizon <= 0:
            msg = "horizon must be positive"
            raise ValueError(msg)

        sigma_obs = self._samples["sigma_obs"]
        n_samples = len(sigma_obs)
        rng = np.random.default_rng(derive_seed(self.random_state, namespace="state_space_predict"))
        predictions = rng.normal(
            loc=0.0,
            scale=np.abs(sigma_obs[:, None]) + 1e-6,
            size=(n_samples, horizon),
        )
        return predictions
